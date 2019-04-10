import logging
import math

import numpy as np
import pandas as pd
from django.db import IntegrityError, transaction

from jrdb.models import Race, choices
from jrdb.templates.parse import filter_na
from jrdb.templates.template import Template
from templates.item import DateTimeItem, ChoiceItem, ForeignKeyItem, IntegerItem, StringItem, InvokeItem

logger = logging.getLogger(__name__)


def symbols(s):
    df = s.copy().to_frame().drop(s.name)

    df['horse_type_symbol'] = s.str[0].map(choices.RACE_HORSE_TYPE_SYMBOL.options())
    df['horse_sex_symbol'] = s.str[1].map(choices.RACE_HORSE_SEX_SYMBOL.options())
    df['interleague_symbol'] = s.str[2].map(choices.RACE_INTERLEAGUE_SYMBOL.options())

    return df


def nth_occurrence(s):
    # casting to float prior to Int64 is necessary
    # to convert strings to numbers
    return s.str.extract(r'([0-9]+)', expand=False) \
        .astype(float) \
        .astype('Int64')


def betting_ticket_sale_flag(s):
    column_map = {
        0: 'sold_win',  # 単勝
        1: 'sold_show',  # 複勝
        2: 'sold_bracket_quinella',  # 枠連
        3: 'sold_quinella',  # 馬連
        4: 'sold_exacta',  # 馬単
        5: 'sold_duet',  # ワイド
        6: 'sold_trio',  # ３連複
        7: 'sold_trifecta'  # ３連単
    }

    return s.str.strip() \
        .map(list) \
        .apply(pd.Series) \
        .astype(float) \
        .applymap(lambda flag: np.nan if math.isnan(flag) else bool(flag)) \
        .rename(columns=column_map)


class BAC(Template):
    """
    レース番組情報

    http://www.jrdb.com/program/Bac/bac_doc.txt
    """
    name = 'JRDB番組データ（BAC）'
    items = [
        ForeignKeyItem('場コード', 2, 0, symbol='jrdb.Race.racetrack', input_symbol='jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, symbol='jrdb.Race.yr'),
        IntegerItem('回', 1, 4, symbol='jrdb.Race.round'),
        StringItem('日', 1, 5, symbol='jrdb.Race.day'),
        IntegerItem('Ｒ', 2, 6, symbol='jrdb.Race.num'),
        DateTimeItem('年月日/発走時間', 12, 8, symbol='jrdb.Race.started_at'),
        IntegerItem('距離', 4, 20, symbol='jrdb.Race.distance'),
        ChoiceItem('芝ダ障害コード', 1, 24, symbol='jrdb.Race.surface', options=choices.SURFACE.options()),
        ChoiceItem('右左', 1, 25, symbol='jrdb.Race.direction', options=choices.DIRECTION.options()),
        ChoiceItem('内外', 1, 26, symbol='jrdb.Race.course_inout', options=choices.COURSE_INOUT.options()),
        ChoiceItem('種別', 2, 27, symbol='jrdb.Race.category', options=choices.RACE_CATEGORY.options()),
        ForeignKeyItem('条件', 2, 29, symbol='jrdb.Race.cond', input_symbol='jrdb.RaceConditionCode.value'),
        InvokeItem('記号', 2, 31, handler=symbols),
        ChoiceItem('重量', 1, 34, symbol='jrdb.Race.impost_class', options=choices.IMPOST_CLASS.options()),
        ChoiceItem('グレード', 1, 35, symbol='jrdb.Race.grade', options=choices.GRADE.options()),
        StringItem('レース名', 50, 36, symbol='jrdb.Race.name'),
        InvokeItem('回数', 8, 86, handler=nth_occurrence),
        IntegerItem('頭数', 2, 94, symbol='jrdb.Race.contender_count'),
        ChoiceItem('コース', 1, 96, symbol='jrdb.Race.course_label', options=choices.COURSE_LABEL.options()),
        ChoiceItem('開催区分', 1, 97, symbol='jrdb.Race.host_category', options=choices.HOST_CATEGORY.options()),
        StringItem('レース名短縮', 8, 98, symbol='jrdb.Race.name_abbr'),
        StringItem('レース名９文字', 18, 106, symbol='jrdb.Race.name_short'),
        # Item('data_category', 'データ区分', 1, 124),
        IntegerItem('１着賞金', 5, 125, symbol='jrdb.Race.p1_purse'),
        IntegerItem('２着賞金', 5, 130, symbol='jrdb.Race.p2_purse'),
        IntegerItem('３着賞金', 5, 135, symbol='jrdb.Race.p3_purse'),
        IntegerItem('４着賞金', 5, 140, symbol='jrdb.Race.p4_purse'),
        IntegerItem('５着賞金', 5, 145, symbol='jrdb.Race.p5_purse'),
        IntegerItem('１着算入賞金', 5, 150, symbol='jrdb.Race.p1_prize'),
        IntegerItem('２着算入賞金', 5, 155, symbol='jrdb.Race.p2_prize'),
        InvokeItem('馬券発売フラグ', 16, 160, handler=betting_ticket_sale_flag),
        IntegerItem('WIN5フラグ', 1, 176, symbol='jrdb.Race.win5'),
    ]

    @transaction.atomic
    def persist(self):
        df = self.clean()
        for row in df.to_dict('records'):
            race = filter_na(row)

            unique_key = {
                'racetrack_id': race.pop('racetrack_id'),
                'yr': race.pop('yr'),
                'round': race.pop('round'),
                'day': race.pop('day'),
                'num': race.pop('num')
            }

            try:
                Race.objects.update_or_create(**unique_key, defaults=race)
            except IntegrityError as e:
                logger.exception(e)
