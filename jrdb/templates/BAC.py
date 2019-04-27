import logging
import math

import numpy as np
import pandas as pd

from ..models import choices
from .item import DateTimeItem, ChoiceItem, ForeignKeyItem, IntegerItem, StringItem, InvokeItem
from .template import Template, RacePersistMixin

logger = logging.getLogger(__name__)


# TODO: Move inline
def symbols(s: pd.Series):
    s1 = s.str[0].map(choices.RACE_HORSE_TYPE_SYMBOL.options()).rename('race__horse_type_symbol')
    s2 = s.str[1].map(choices.RACE_HORSE_SEX_SYMBOL.options()).rename('race__horse_sex_symbol')
    s3 = s.str[2].map(choices.RACE_INTERLEAGUE_SYMBOL.options()).rename('race__interleague_symbol')
    return pd.concat([s1, s2, s3], axis='columns')


# TODO: Move inline
def nth_occurrence(s: pd.Series):
    # casting to float prior to Int64 is necessary
    # to convert strings to numbers
    return s.str.extract(r'([0-9]+)', expand=False) \
        .astype(float) \
        .astype('Int64') \
        .rename('race__nth_occurrence')


# TODO: Move inline
def betting_ticket_sale_flag(s: pd.Series):
    colmap = {
        0: 'race__sold_win',  # 単勝
        1: 'race__sold_show',  # 複勝
        2: 'race__sold_bracket_quinella',  # 枠連
        3: 'race__sold_quinella',  # 馬連
        4: 'race__sold_exacta',  # 馬単
        5: 'race__sold_duet',  # ワイド
        6: 'race__sold_trio',  # ３連複
        7: 'race__sold_trifecta'  # ３連単
    }

    return s.str.strip() \
        .map(list) \
        .apply(pd.Series) \
        .astype(float) \
        .applymap(lambda flag: np.nan if math.isnan(flag) else bool(flag)) \
        .rename(columns=colmap)


class BAC(Template, RacePersistMixin):
    """
    レース番組情報

    http://www.jrdb.com/program/Bac/bac_doc.txt
    """
    name = 'JRDB番組データ（BAC）'
    items = [
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Program.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Program.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Program.round'),
        StringItem('日', 1, 5, 'jrdb.Program.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        DateTimeItem('年月日/発走時間', 12, 8, 'jrdb.Race.started_at'),
        IntegerItem('距離', 4, 20, 'jrdb.Race.distance'),
        ChoiceItem('芝ダ障害コード', 1, 24, 'jrdb.Race.surface', choices.SURFACE.options()),
        ChoiceItem('右左', 1, 25, 'jrdb.Race.direction', choices.DIRECTION.options()),
        ChoiceItem('内外', 1, 26, 'jrdb.Race.course_inout', choices.COURSE_INOUT.options()),
        ChoiceItem('種別', 2, 27, 'jrdb.Race.category', choices.RACE_CATEGORY.options()),
        ForeignKeyItem('条件', 2, 29, 'jrdb.Race.cond', 'jrdb.RaceConditionCode.value'),
        InvokeItem('記号', 2, 31, symbols),
        ChoiceItem('重量', 1, 34, 'jrdb.Race.impost_class', choices.IMPOST_CLASS.options()),
        ChoiceItem('グレード', 1, 35, 'jrdb.Race.grade', choices.GRADE.options()),
        StringItem('レース名', 50, 36, 'jrdb.Race.name'),
        InvokeItem('回数', 8, 86, nth_occurrence),
        IntegerItem('頭数', 2, 94, 'jrdb.Race.contender_count'),
        ChoiceItem('コース', 1, 96, 'jrdb.Race.course_label', choices.COURSE_LABEL.options()),
        ChoiceItem('開催区分', 1, 97, 'jrdb.Race.host_category', choices.HOST_CATEGORY.options()),
        StringItem('レース名短縮', 8, 98, 'jrdb.Race.name_abbr'),
        StringItem('レース名９文字', 18, 106, 'jrdb.Race.name_short'),
        # Item('data_category', 'データ区分', 1, 124),
        IntegerItem('１着賞金', 5, 125, 'jrdb.Race.p1_purse'),
        IntegerItem('２着賞金', 5, 130, 'jrdb.Race.p2_purse'),
        IntegerItem('３着賞金', 5, 135, 'jrdb.Race.p3_purse'),
        IntegerItem('４着賞金', 5, 140, 'jrdb.Race.p4_purse'),
        IntegerItem('５着賞金', 5, 145, 'jrdb.Race.p5_purse'),
        IntegerItem('１着算入賞金', 5, 150, 'jrdb.Race.p1_prize'),
        IntegerItem('２着算入賞金', 5, 155, 'jrdb.Race.p2_prize'),
        InvokeItem('馬券発売フラグ', 16, 160, betting_ticket_sale_flag),
        IntegerItem('WIN5フラグ', 1, 176, 'jrdb.Race.win5'),
    ]
