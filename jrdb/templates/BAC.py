import logging
import math

import numpy as np
import pandas as pd
from django.db import IntegrityError, transaction

from jrdb.models import Race, choices
from jrdb.templates.parse import filter_na
from jrdb.templates.template import Template, Item

logger = logging.getLogger(__name__)


class BAC(Template):
    """
    レース番組情報

    http://www.jrdb.com/program/Bac/bac_doc.txt
    """
    name = 'JRDB番組データ（BAC）'
    items = [
        Item('jrdb.Race.racetrack.code', '場コード', 2, 0),
        Item('jrdb.Race.yr', '年', 2, 2),
        Item('jrdb.Race.round', '回', 1, 4),
        Item('jrdb.Race.day', '日', 1, 5),
        Item('jrdb.Race.num', 'Ｒ', 2, 6),
        Item('start_date', '年月日', 8, 8, notes='YYYYMMDD'),
        Item('start_time', '発走時間', 4, 16, notes='HHMM', use=False),
        Item('jrdb.Race.distance', '距離', 4, 20),
        Item('jrdb.Race.surface', '芝ダ障害コード', 1, 24, notes='1:芝, 2:ダート, 3:障害', options=choices.SURFACE.options()),
        Item('jrdb.Race.direction', '右左', 1, 25, notes='1:右, 2:左, 3:直, 9:他', options=choices.DIRECTION.options()),
        Item('jrdb.Race.course_inout', '内外', 1, 26, options=choices.COURSE_INOUT.options(),
             notes='1:通常(内), 2:外, 3,直ダ, 9:他\n※障害のトラックは、以下の２通りとなります。\n"393":障害直線ダート\n"391":障害直線芝'),
        Item('jrdb.Race.category', '種別', 2, 27, notes='４歳以上等、→JRDBデータコード表', options=choices.RACE_CATEGORY.options()),
        Item('jrdb.Race.cond.value', '条件', 2, 29, notes='900万下等、 →JRDBデータコード表'),
        Item('symbols', '記号', 2, 31, notes='○混等、 →JRDBデータコード表'),
        Item('jrdb.Race.impost_class', '重量', 1, 34, notes='ハンデ等、 →JRDBデータコード表', options=choices.IMPOST_CLASS.options()),
        Item('jrdb.Race.grade', 'グレード', 1, 35, notes='Ｇ１等 →JRDBデータコード表', options=choices.GRADE.options()),
        Item('jrdb.Race.name', 'レース名', 50, 36, notes='レース名の通称（全角２５文字）'),
        Item('jrdb.Race.nth_occurrence', '回数', 8, 86, notes='第ZZ9回（全角半角混在）'),
        Item('jrdb.Race.contender_count', '頭数', 2, 94),
        Item('jrdb.Race.course_label', 'コース', 1, 96, notes='1:A, 2:A1, 3:A2, 4:B, 5:C, 6:D',
             options=choices.COURSE_LABEL.options()),
        Item('jrdb.Race.host_category', '開催区分', 1, 97, notes='1:関東, 2:関西, 3:ローカル',
             options=choices.HOST_CATEGORY.options()),
        Item('jrdb.Race.name_abbr', 'レース名短縮', 8, 98, notes='全角４文字'),
        Item('jrdb.Race.name_short', 'レース名９文字', 18, 106, notes='全角９文字'),
        Item('data_category', 'データ区分', 1, 124, notes='1:特別登録, 2:想定確定, 3:前日', use=False),
        Item('jrdb.Race.p1_purse', '１着賞金', 5, 125, notes='単位（万円）'),
        Item('jrdb.Race.p2_purse', '２着賞金', 5, 130, notes='単位（万円）'),
        Item('jrdb.Race.p3_purse', '３着賞金', 5, 135, notes='単位（万円）'),
        Item('jrdb.Race.p4_purse', '４着賞金', 5, 140, notes='単位（万円）'),
        Item('jrdb.Race.p5_purse', '５着賞金', 5, 145, notes='単位（万円）'),
        Item('jrdb.Race.p1_prize', '１着算入賞金', 5, 150, notes='単位（万円）'),
        Item('jrdb.Race.p2_prize', '２着算入賞金', 5, 155, notes='単位（万円）'),
        Item('betting_ticket_sale_flag', '馬券発売フラグ', 16, 160, notes='1:発売, 0:発売無し'),
        Item('jrdb.Race.win5', 'WIN5フラグ', 1, 176, notes='1～5'),
        Item('reserved', '予備', 5, 177, notes='スペース', use=False),
        Item('newline', '改行', 2, 182, notes='ＣＲ・ＬＦ', use=False),
    ]

    def clean_start_date(self) -> pd.Series:
        started_at = self.df.start_date + self.df.start_time
        return pd.to_datetime(started_at, format='%Y%m%d%H%M').dt.tz_localize('Asia/Tokyo').rename('started_at')

    def clean_symbols(self):
        df = pd.DataFrame(index=self.df.index)

        df['horse_type_symbol'] = self.df.symbols.str[0].map(choices.RACE_HORSE_TYPE_SYMBOL.options())
        df['horse_sex_symbol'] = self.df.symbols.str[1].map(choices.RACE_HORSE_SEX_SYMBOL.options())
        df['interleague_symbol'] = self.df.symbols.str[2].map(choices.RACE_INTERLEAGUE_SYMBOL.options())

        return df

    def clean_nth_occurrence(self):
        # casting to float prior to Int64 is necessary
        # to convert strings to numbers
        return self.df.nth_occurrence.str.extract(r'([0-9]+)', expand=False) \
            .astype(float) \
            .astype('Int64')

    def clean_betting_ticket_sale_flag(self):
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

        return self.df.betting_ticket_sale_flag.str.strip() \
            .map(list) \
            .apply(pd.Series) \
            .astype(float) \
            .applymap(lambda flag: np.nan if math.isnan(flag) else bool(flag)) \
            .rename(columns=column_map)

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
