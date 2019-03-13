import pandas as pd
from django.db import IntegrityError

from jrdb.models import RacetrackCode, Race, RaceCategoryCode, RaceConditionCode, ImpostClassCode, GradeCode
from jrdb.templates.parse import filter_na
from jrdb.templates.template import Template


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
        ['', '回数', None, '8', 'X', '87', '第ZZ9回（全角半角混在）'],
        ['contender_count', '頭数', None, '2', '99', '95', None],
        ['course_label', 'コース', None, '1', 'X', '97', '1:A, 2:A1, 3:A2, 4:B, 5:C, 6:D'],
        ['', '開催区分', None, '1', 'X', '98', '1:関東, 2:関西, 3:ローカル'],
        ['race_name_abbr', 'レース名短縮', None, '8', 'X', '99', '全角４文字'],
        ['race_name_short', 'レース名９文字', None, '18', 'X', '107', '全角９文字'],
        ['', 'データ区分', None, '1', 'X', '125', '1:特別登録, 2:想定確定, 3:前日'],
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
        ['win5_flag', 'WIN5フラグ', None, '1', 'Z', '177', '1～5'],
        ['reserved', '予備', None, '5', 'X', '178', 'スペース'],
        ['newline', '改行', None, '2', 'X', '183', 'ＣＲ・ＬＦ']
    ]

    def clean(self):
        df = self.df[['racetrack_code']]

        racetrack_codes = RacetrackCode.objects.filter(key__in=self.df.racetrack_code)
        racetrack_code_map = {code.key: code.id for code in racetrack_codes}
        df['racetrack_id'] = df.racetrack_code.map(racetrack_code_map).astype(int)
        df.drop(columns=['racetrack_code'], inplace=True)

        df['yr'] = self.df.yr.astype(int)
        df['round'] = self.df['round'].astype(int)
        df['day'] = self.df.day.astype(int)
        df['num'] = self.df.num.astype(int)

        started_at = self.df.start_date + self.df.start_time
        df['started_at'] = pd.to_datetime(started_at, format='%Y%m%d%H%M').dt.tz_localize('Asia/Tokyo')

        df['distance'] = self.df.distance.astype(int)
        df['surface'] = self.df.surface.astype(int).map({1: Race.TURF, 2: Race.DIRT, 3: Race.OBSTACLE})

        df['direction'] = self.df.direction.astype(int).map({
            1: Race.RIGHT,
            2: Race.LEFT,
            3: Race.STRAIGHT,
            4: Race.OTHER
        })

        df['course_inout'] = self.df.course_inout.astype(int).map({
            1: Race.INSIDE,
            2: Race.OUTSIDE,
            3: Race.STRAIGHT_DIRT,
            9: Race.OTHER
        })

        category_codes = RaceCategoryCode.objects.filter(key__in=self.df.race_category_code)
        category_code_map = {code.key: code.id for code in category_codes}
        df['category_id'] = self.df.race_category_code.map(category_code_map).astype(int)

        cond_codes = RaceConditionCode.objects.filter(key__in=self.df.race_cond_code)
        cond_code_map = {code.key: code.id for code in cond_codes}
        df['cond_id'] = self.df.race_cond_code.map(cond_code_map).astype(int)

        # TODO: race symbols

        impost_class_codes = ImpostClassCode.objects.filter(key__in=self.df.impost_class_code)
        impost_class_code_map = {code.key: code.id for code in impost_class_codes}
        df['impost_class_id'] = self.df.impost_class_code.map(impost_class_code_map).astype(int)

        grade_codes = GradeCode.objects.filter(key__in=self.df.grade_code)
        grade_code_map = {code.key: code.id for code in grade_codes}
        df['grade_id'] = self.df.grade_code.map(grade_code_map).astype('Int64')

        df['name'] = self.df.race_name.str.strip()
        df['name_short'] = self.df.race_name_short.str.strip()
        df['name_abbr'] = self.df.race_name_abbr.str.strip()

        return df

    def persist(self):
        df = self.clean()
        for row in df.to_dict('records'):
            obj = filter_na(row)
            try:
                Race.objects.create(**obj)
            except IntegrityError:
                Race.objects.filter(
                    racetrack_id=obj['racetrack_id'],
                    yr=obj['yr'],
                    round=obj['round'],
                    day=obj['day'],
                    num=obj['num']
                ).update(**obj)
