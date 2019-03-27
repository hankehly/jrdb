import logging
import math

import numpy as np
import pandas as pd
from django.db import IntegrityError

from jrdb.models import Race, RaceConditionCode, Racetrack
from jrdb.models.choices import (
    RACE_CATEGORY,
    RACE_HORSE_TYPE_SYMBOL,
    RACE_HORSE_SEX_SYMBOL,
    RACE_INTERLEAGUE_SYMBOL,
    IMPOST_CLASS,
    GRADE,
    SURFACE,
    DIRECTION,
    COURSE_INOUT,
    COURSE_LABEL,
    HOST_CATEGORY)
from jrdb.templates.parse import filter_na, parse_int_or
from jrdb.templates.template import Template

logger = logging.getLogger(__name__)


class BAC(Template):
    """
    レース番組情報

    http://www.jrdb.com/program/Bac/bac_doc.txt
    """
    name = 'JRDB番組データ（BAC）'
    items = [
        ['racetrack_code', '場コード', None, '2', '99', '1', None],
        ['yr', '年', None, '2', '99', '3', None],
        ['round', '回', None, '1', '9', '5', None],
        ['day', '日', None, '1', 'F', '6', None],
        ['num', 'Ｒ', None, '2', '99', '7', None],
        ['start_date', '年月日', None, '8', '9', '9', 'YYYYMMDD'],
        ['start_time', '発走時間', None, '4', 'X', '17', 'HHMM'],
        ['distance', '距離', None, '4', '9999', '21', None],
        ['surface', '芝ダ障害コード', None, '1', '9', '25', '1:芝, 2:ダート, 3:障害'],
        ['direction', '右左', None, '1', '9', '26', '1:右, 2:左, 3:直, 9:他'],
        ['course_inout', '内外', None, '1', '9', '27',
         '1:通常(内), 2:外, 3,直ダ, 9:他\n※障害のトラックは、以下の２通りとなります。\n"393":障害直線ダート\n"391":障害直線芝'],
        ['race_category_code', '種別', None, '2', '99', '28', '４歳以上等、→JRDBデータコード表'],
        ['race_cond_code', '条件', None, '2', 'XX', '30', '900万下等、 →JRDBデータコード表'],
        ['race_symbols', '記号', None, '3', '999', '32', '○混等、 →JRDBデータコード表'],
        ['impost_class_code', '重量', None, '1', '9', '35', 'ハンデ等、 →JRDBデータコード表'],
        ['grade_code', 'グレード', None, '1', '9', '36', 'Ｇ１等 →JRDBデータコード表'],
        ['race_name', 'レース名', None, '50', 'X', '37', 'レース名の通称（全角２５文字）'],
        ['nth_occurrence', '回数', None, '8', 'X', '87', '第ZZ9回（全角半角混在）'],
        ['contender_count', '頭数', None, '2', '99', '95', None],
        ['course_label', 'コース', None, '1', 'X', '97', '1:A, 2:A1, 3:A2, 4:B, 5:C, 6:D'],
        ['host_category', '開催区分', None, '1', 'X', '98', '1:関東, 2:関西, 3:ローカル'],
        ['race_name_abbr', 'レース名短縮', None, '8', 'X', '99', '全角４文字'],
        ['race_name_short', 'レース名９文字', None, '18', 'X', '107', '全角９文字'],
        ['data_category', 'データ区分', None, '1', 'X', '125', '1:特別登録, 2:想定確定, 3:前日'],
        ['p1_purse', '１着賞金', None, '5', 'ZZZZ9', '126', '単位（万円）'],
        ['p2_purse', '２着賞金', None, '5', 'ZZZZ9', '131', '単位（万円）'],
        ['p3_purse', '３着賞金', None, '5', 'ZZZZ9', '136', '単位（万円）'],
        ['p4_purse', '４着賞金', None, '5', 'ZZZZ9', '141', '単位（万円）'],
        ['p5_purse', '５着賞金', None, '5', 'ZZZZ9', '146', '単位（万円）'],
        ['p1_prize', '１着算入賞金', None, '5', 'ZZZZ9', '151', '単位（万円）'],
        ['p2_prize', '２着算入賞金', None, '5', 'ZZZZ9', '156', '単位（万円）'],
        # 1バイト目 単勝
        # 2バイト目 複勝
        # 3バイト目 枠連
        # 4バイト目 馬連
        # 5バイト目 馬単
        # 6バイト目 ワイド
        # 7バイト目 ３連複
        # 8バイト目 ３連単
        # 9-16バイト目　予備
        ['betting_ticket_sale_flag', '馬券発売フラグ', None, '16', '9', '161', '1:発売, 0:発売無し'],
        ['win5', 'WIN5フラグ', None, '1', 'Z', '177', '1～5'],
        ['reserved', '予備', None, '5', 'X', '178', 'スペース'],
        ['newline', '改行', None, '2', 'X', '183', 'ＣＲ・ＬＦ']
    ]

    def clean(self):
        racetracks = Racetrack.objects.filter(code__in=self.df.racetrack_code).values('code', 'id')
        s = self.df.racetrack_code.map({racetrack['code']: racetrack['id'] for racetrack in racetracks})
        s.name = 'racetrack_id'

        df = s.to_frame()

        df['yr'] = self.df.yr.astype(int)
        df['round'] = self.df['round'].astype(int)
        df['day'] = self.df.day.str.strip()
        df['num'] = self.df.num.astype(int)
        df['started_at'] = self._started_at()
        df['distance'] = self.df.distance.astype(int)
        df['surface'] = self.df.surface.map(SURFACE.get_key_map())
        df['direction'] = self.df.direction.map(DIRECTION.get_key_map())
        df['course_inout'] = self.df.course_inout.map(COURSE_INOUT.get_key_map())
        df['course_label'] = self.df.course_label.map(COURSE_LABEL.get_key_map())
        df['host_category'] = self.df.host_category.map(HOST_CATEGORY.get_key_map())
        df['category'] = self.df.race_category_code.map(RACE_CATEGORY.get_key_map())
        df['cond_id'] = RaceConditionCode.key2id(self.df.race_cond_code)
        df['horse_type_symbol'] = self.df.race_symbols.str[0].map(RACE_HORSE_TYPE_SYMBOL.get_key_map())
        df['horse_sex_symbol'] = self.df.race_symbols.str[1].map(RACE_HORSE_SEX_SYMBOL.get_key_map())
        df['interleague_symbol'] = self.df.race_symbols.str[2].map(RACE_INTERLEAGUE_SYMBOL.get_key_map())
        df['impost_class'] = self.df.impost_class_code.map(IMPOST_CLASS.get_key_map())
        df['grade'] = self.df.grade_code.map(GRADE.get_key_map())

        df['name'] = self.df.race_name.str.strip()
        df['name_short'] = self.df.race_name_short.str.strip()
        df['name_abbr'] = self.df.race_name_abbr.str.strip()

        # casting to float prior to Int64 is necessary
        # to convert strings to numbers
        df['nth_occurrence'] = self.df.nth_occurrence.str.extract(r'([0-9]+)', expand=False) \
            .astype(float) \
            .astype('Int64')

        df['contender_count'] = self.df.contender_count.astype(int)

        df['p1_purse'] = self.df.p1_purse.astype(int)
        df['p2_purse'] = self.df.p2_purse.astype(int)
        df['p3_purse'] = self.df.p3_purse.astype(int)
        df['p4_purse'] = self.df.p4_purse.astype(int)
        df['p5_purse'] = self.df.p5_purse.astype(int)
        df['p1_prize'] = self.df.p1_prize.astype(int)
        df['p2_prize'] = self.df.p2_prize.astype(int)

        df['win5'] = self.df.win5.apply(parse_int_or, args=(np.nan,)).astype('Int64')

        betting_ticket_columns = {
            0: 'issued_bt_win',
            1: 'issued_bt_show',
            2: 'issued_bt_bracket_quinella',
            3: 'issued_bt_quinella',
            4: 'issued_bt_exacta',
            5: 'issued_bt_duet',
            6: 'issued_bt_trio',
            7: 'issued_bt_trifecta'
        }

        betting_ticket_flags = self.df.betting_ticket_sale_flag.str.strip() \
            .map(list) \
            .apply(pd.Series) \
            .astype(float) \
            .applymap(lambda flag: np.nan if math.isnan(flag) else bool(flag)) \
            .rename(columns=betting_ticket_columns)

        return df.join(betting_ticket_flags)

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

    def _started_at(self) -> pd.Series:
        started_at = self.df.start_date + self.df.start_time
        return pd.to_datetime(started_at, format='%Y%m%d%H%M').dt.tz_localize('Asia/Tokyo').rename('started_at')
