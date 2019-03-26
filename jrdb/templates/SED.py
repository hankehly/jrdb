import numpy as np
import pandas as pd
from django.db import IntegrityError

from jrdb.models import RaceConditionCode, Jockey, PaceFlowCode, Racetrack, Trainer, Race, Contender, Horse
from jrdb.models.choices import (
    PACE_CATEGORY,
    SURFACE,
    DIRECTION,
    COURSE_INOUT,
    COURSE_LABEL,
    TRACK_CONDITION,
    RACE_CATEGORY,
    RACE_HORSE_TYPE_SYMBOL,
    RACE_HORSE_SEX_SYMBOL,
    RACE_INTERLEAGUE_SYMBOL,
    IMPOST_CLASS,
    GRADE,
    WEATHER,
    PENALTY,
    RACE_LINE,
    IMPROVEMENT,
    PHYSIQUE,
    DEMEANOR,
    RUNNING_STYLE
)
from jrdb.templates.parse import parse_int_or, parse_float_or, filter_na
from jrdb.templates.template import Template


class SED(Template):
    """
    http://www.jrdb.com/program/Sed/sed_doc.txt

    The "種別" values in the above document are incorrect.
    The correct values can be found [here](http://www.jrdb.com/program/jrdb_code.txt)
    """
    name = 'JRDB成績データ（SED）'

    items = [
        # レースキー
        ['racetrack_code', '場コード', None, '2', '99', '1', None],
        ['yr', '年', None, '2', '99', '3', None],
        ['round', '回', None, '1', '9', '5', None],
        ['day', '日', None, '1', 'F', '6', None],
        ['race_num', 'Ｒ', None, '2', '99', '7', None],
        ['horse_num', '馬番', None, '2', '99', '9', None],
        ['pedigree_reg_num', '血統登録番号', None, '8', 'X', '11', None],
        ['race_date', '年月日', None, '8', '9', '19', 'YYYYMMDD <-暫定版より順序'],  # IGNORED (use value from BAC)
        ['horse_name', '馬名', None, '36', 'X', '27', '全角１８文字 <-入れ替え'],
        # レース条件
        ['race_distance', '距離', None, '4', '9999', '63', None],
        ['race_surface_code', '芝ダ障害コード', None, '1', '9', '67', '1:芝, 2:ダート, 3:障害'],
        ['race_direction', '右左', None, '1', '9', '68', '1:右, 2:左, 3:直, 9:他'],
        ['race_course_inout', '内外', None, '1', '9', '69',
         '1:通常(内), 2:外, 3,直ダ, 9:他\n※障害のトラックは、以下の２通りとなります。\n"393":障害直線ダート\n"391":障害直線芝'],
        ['race_track_cond_code', '馬場状態', None, '2', '99', '70', None],
        ['race_category_code', '種別', None, '2', '99', '72', '４歳以上等、→成績データの説明'],
        ['race_cond_code', '条件', None, '2', 'XX', '74', '900万下等、 →成績データの説明'],
        ['race_symbols', '記号', None, '3', '999', '76', '○混等、 →成績データの説明'],
        ['race_impost_class_code', '重量', None, '1', '9', '79', 'ハンデ等、 →成績データの説明'],
        ['race_grade', 'グレード', None, '1', '9', '80', None],
        ['race_name', 'レース名', None, '50', 'X', '81', 'レース名の通称（全角２５文字）'],
        ['race_contender_count', '頭数', None, '2', '99', '131', None],
        ['race_name_abbr', 'レース名略称', None, '8', 'X', '133', '全角４文字'],
        # 馬成績
        ['order_of_finish', '着順', None, '2', '99', '141', None],
        ['penalty_code', '異常区分', None, '1', '9', '143', None],
        ['time', 'タイム', None, '4', '9999', '144', '1byte:分, 2-4byte:秒(0.1秒単位)'],
        ['mounted_weight', '斤量', None, '3', '999', '148', '0.1Kg単位'],
        ['jockey_name', '騎手名', None, '12', 'X', '151', '全角６文字'],
        ['trainer_name', '調教師名', None, '12', 'X', '163', '全角６文字'],
        ['fin_win_odds', '確定単勝オッズ', None, '6', 'ZZZ9.9', '175', None],
        ['fin_win_pop', '確定単勝人気順位', None, '2', '99', '181', None],
        # ＪＲＤＢデータ
        ['IDM', 'ＩＤＭ', None, '3', 'ZZ9', '183', None],
        ['speed_index', '素点', None, '3', 'ZZ9', '186', None],
        ['track_speed_shift', '馬場差', None, '3', 'ZZ9', '189', None],
        ['pace', 'ペース', None, '3', 'ZZZ', '192', None],
        ['late_start', '出遅', None, '3', 'ZZZ', '195', None],
        ['positioning', '位置取', None, '3', 'ZZZ', '198', None],
        ['disadvt', '不利', None, '3', 'ZZZ', '201', None],
        ['b3f_disadvt', '前不利', None, '3', 'ZZZ', '204', '前３Ｆ内での不利'],
        ['mid_disadvt', '中不利', None, '3', 'ZZZ', '207', '道中での不利'],
        ['f3f_disadvt', '後不利', None, '3', 'ZZZ', '210', '後３Ｆ内での不利'],
        # 単位/意味不明
        ['race_ind', 'レース', None, '3', 'ZZZ', '213', None],  # IGNORED
        ['race_line', 'コース取り', None, '1', '9', '216', '1:最内,2:内,3:中,4:外,5:大外'],
        ['improvement_code', '上昇度コード', None, '1', '9', '217', '1:AA, 2:A, 3:B, 4:C, 5:?'],
        # TODO: Why does race_class_code differ between horses in the same race?
        ['race_class_code', 'クラスコード', None, '2', '99', '218', None],  # IGNORED
        ['horse_physique_code', '馬体コード', None, '1', '9', '220', None],
        ['horse_demeanor_code', '気配コード', None, '1', '9', '221', None],
        ['race_pace', 'レースペース', None, '1', 'X', '222', 'H:ハイ, M:平均, S:スロー'],
        ['horse_pace', '馬ペース', None, '1', 'X', '223', '馬自身のペース(H:M:S)'],
        # テン指数はダッシュ力を意味する（元になる数値は前３Ｆタイム）
        ['b3f_time_index', 'テン指数', None, '5', 'ZZ9.9', '224', '前３Ｆタイムを指数化したもの'],
        # 勝負所からの最後の脚（元になる数値は後3Fタイム）
        ['f3f_time_index', '上がり指数', None, '5', 'ZZ9.9', '229', '後３Ｆタイムを指数化したもの'],
        # ペース指数は道中どれぐらいのペースで後３Ｆを走ったか（元になる数値は走破タイム-後3Fタイム）
        ['horse_pace_index', 'ペース指数', None, '5', 'ZZ9.9', '234', '馬のペースを指数化したもの'],
        ['race_pace_index', 'レースＰ指数', None, '5', 'ZZ9.9', '239', 'レースのペースを指数化したもの'],
        # for 1st place horses, the second place horse name/time
        # for 2nd > place horses, the first place horse name/time
        ['fos_horse_name', '1(2)着馬名', None, '12', 'X', '244', '全角６文字'],  # IGNORED
        ['margin', '1(2)着タイム差', None, '3', '999', '256', '0.1秒単位'],
        ['b3f_time', '前３Ｆタイム', None, '3', '999', '259', '0.1秒単位'],
        ['f3f_time', '後３Ｆタイム', None, '3', '999', '262', '0.1秒単位'],
        ['note', '備考', None, '24', 'X', '265', '全角１２文字（地方競馬場名等）'],  # IGNORED
        ['reserved_0', '予備', None, '2', 'X', '289', 'スペース'],
        ['fin_show_odds_lower_limit', '確定複勝オッズ下', None, '6', 'ZZZ9.9', '291', '最終的な複勝オッズ（下限）'],  # IGNORED
        ['win_odds_10am', '10時単勝オッズ', None, '6', 'ZZZ9.9', '297', '10時頃の単勝オッズ'],  # IGNORED
        ['show_odds_10am', '10時複勝オッズ', None, '6', 'ZZZ9.9', '303', '10時頃の複勝オッズ'],  # IGNORED
        ['c1p', 'コーナー順位１', None, '2', '99', '309', None],
        ['c2p', 'コーナー順位２', None, '2', '99', '311', None],
        ['c3p', 'コーナー順位３', None, '2', '99', '313', None],
        ['c4p', 'コーナー順位４', None, '2', '99', '315', None],
        ['b3f_1p_margin', '前３Ｆ先頭差', None, '3', '99', '317', '前３Ｆ地点での先頭とのタイム差\n0.1秒単位'],
        ['f3f_1p_margin', '後３Ｆ先頭差', None, '3', '99', '320', '後３Ｆ地点での先頭とのタイム差\n0.1秒単位'],
        ['jockey_code', '騎手コード', None, '5', '9', '323', '騎手マスタとリンク'],
        ['trainer_code', '調教師コード', None, '5', '9', '328', '調教師マスタとリンク'],
        ['horse_weight', '馬体重', None, '3', '999', '333', 'データ無:スペース'],
        ['horse_weight_diff', '馬体重増減', None, '3', 'XZ9', '336', '符号+数字２桁、データ無:スペース'],
        ['weather_code', '天候コード', None, '1', '9', '339', 'コード表参照'],
        ['course_label', 'コース', None, '1', 'X', '340', '1:A,2:A1,3:A2,4:B,5:C,6:D'],
        ['running_style_code', 'レース脚質', None, '1', 'X', '341', '脚質コード参照'],
        ['win_payoff_yen', '単勝', None, '7', 'ZZZZZZ9', '342', '単位（円）'],  # IGNORED
        ['show_payoff_yen', '複勝', None, '7', 'ZZZZZZ9', '349', '単位（円）'],  # IGNORED
        ['purse', '本賞金', None, '5', 'ZZZZ9', '356', '単位（万円）'],
        ['p1_prize', '収得賞金', None, '5', 'ZZZZ9', '361', '単位（万円）'],
        ['race_pace_flow_code', 'レースペース流れ', None, '2', '99', '366', '→成績データの説明'],
        ['horse_pace_flow_code', '馬ペース流れ', None, '2', '99', '368', '→成績データの説明'],
        ['c4_race_line', '４角コース取り', None, '1', '9', '370', '1:最内,2:内,3:中,4:外,5:大外'],
        ['reserved_1', '予備', None, '4', 'X', '371', 'スペース'],
        ['newline', '改行', None, '2', 'X', '375', 'ＣＲ・ＬＦ']
    ]

    def clean(self):
        # Race
        racetracks = Racetrack.objects.filter(code__in=self.df.racetrack_code).values('code', 'id')
        s = self.df.racetrack_code.map({racetrack['code']: racetrack['id'] for racetrack in racetracks})
        s.name = 'racetrack_id'

        rdf = s.to_frame()
        rdf['yr'] = self.df.yr.astype(int)
        rdf['round'] = self.df['round'].astype(int)
        rdf['day'] = self.df.day.str.strip()
        rdf['num'] = self.df.race_num.astype(int)
        rdf['distance'] = self.df.race_distance.astype(int)
        rdf['surface'] = self.df.race_surface_code.map(SURFACE.get_key_map())
        rdf['direction'] = self.df.race_direction.map(DIRECTION.get_key_map())
        rdf['course_inout'] = self.df.race_course_inout.map(COURSE_INOUT.get_key_map())
        rdf['track_cond'] = self.df.race_track_cond_code.map(TRACK_CONDITION.get_key_map())
        rdf['category'] = self.df.race_category_code.map(RACE_CATEGORY.get_key_map())
        rdf['cond_id'] = RaceConditionCode.key2id(self.df.race_cond_code)
        rdf['horse_type_symbol'] = self.df.race_symbols.str[0].map(RACE_HORSE_TYPE_SYMBOL.get_key_map())
        rdf['horse_sex_symbol'] = self.df.race_symbols.str[1].map(RACE_HORSE_SEX_SYMBOL.get_key_map())
        rdf['interleague_symbol'] = self.df.race_symbols.str[2].map(RACE_INTERLEAGUE_SYMBOL.get_key_map())
        rdf['impost_class'] = self.df.race_impost_class_code.map(IMPOST_CLASS.get_key_map())
        rdf['grade'] = self.df.race_grade.map(GRADE.get_key_map())
        rdf['name'] = self.df.race_name.str.strip()
        rdf['name_abbr'] = self.df.race_name_abbr.str.strip()
        rdf['track_speed_shift'] = self.df.track_speed_shift.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        rdf['pace_cat'] = self.df.race_pace.map(PACE_CATEGORY.get_key_map())
        rdf['pace_index'] = self.df.race_pace_index.apply(parse_float_or, args=(np.nan,))
        rdf['weather'] = self.df.weather_code.map(WEATHER.get_key_map())
        rdf['course_label'] = self.df.course_label.map(COURSE_LABEL.get_key_map())
        rdf['pace_flow_id'] = PaceFlowCode.key2id(self.df.race_pace_flow_code, allow_null=True)

        # Contender
        cdf = pd.DataFrame(index=rdf.index)
        cdf['num'] = self.df.horse_num.astype(int)
        cdf['order_of_finish'] = self.df.order_of_finish.astype(int)
        cdf['penalty'] = self.df.penalty_code.map(PENALTY.get_key_map())
        cdf['time'] = self.df.time.str.strip().where(lambda x: x != '').astype(float) * 0.1
        cdf['mounted_weight'] = self.df.mounted_weight.astype(int) * 0.1
        cdf['odds_win'] = self.df.fin_win_odds.apply(parse_float_or, args=(np.nan,))
        cdf['popularity'] = self.df.fin_win_pop.astype(int)
        cdf['IDM'] = self.df.IDM.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['speed_index'] = self.df.speed_index.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['pace'] = self.df.pace.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['positioning'] = self.df.positioning.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['disadvt'] = self.df.disadvt.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['b3f_disadvt'] = self.df.b3f_disadvt.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['mid_disadvt'] = self.df.mid_disadvt.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['f3f_disadvt'] = self.df.f3f_disadvt.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['race_line'] = self.df.race_line.map(RACE_LINE.get_key_map())
        cdf['improvement'] = self.df.improvement_code.map(IMPROVEMENT.get_key_map())
        cdf['physique'] = self.df.horse_physique_code.map(PHYSIQUE.get_key_map())
        cdf['demeanor'] = self.df.horse_demeanor_code.map(DEMEANOR.get_key_map())
        cdf['pace_cat'] = self.df.horse_pace.map(PACE_CATEGORY.get_key_map())
        cdf['b3f_time_index'] = self.df.b3f_time_index.apply(parse_float_or, args=(np.nan,))
        cdf['f3f_time_index'] = self.df.f3f_time_index.apply(parse_float_or, args=(np.nan,))
        cdf['pace_index'] = self.df.horse_pace_index.apply(parse_float_or, args=(np.nan,))
        cdf['margin'] = self.df.margin.apply(parse_float_or, args=(np.nan,)) * 0.1
        cdf['b3f_time'] = self.df.b3f_time.apply(parse_float_or, args=(np.nan,)) * 0.1
        cdf['f3f_time'] = self.df.f3f_time.apply(parse_float_or, args=(np.nan,)) * 0.1
        cdf['c1p'] = self.df.c1p.apply(parse_float_or, args=(np.nan,)).where(lambda x: x != 0).astype('Int64')
        cdf['c2p'] = self.df.c2p.apply(parse_float_or, args=(np.nan,)).where(lambda x: x != 0).astype('Int64')
        cdf['c3p'] = self.df.c3p.apply(parse_float_or, args=(np.nan,)).where(lambda x: x != 0).astype('Int64')
        cdf['c4p'] = self.df.c4p.apply(parse_float_or, args=(np.nan,)).where(lambda x: x != 0).astype('Int64')
        cdf['b3f_1p_margin'] = self.df.b3f_1p_margin.apply(parse_float_or, args=(np.nan,)) * 0.1
        cdf['f3f_1p_margin'] = self.df.f3f_1p_margin.apply(parse_float_or, args=(np.nan,)) * 0.1

        cdf['jockey_code'] = self.df.jockey_code.str.strip()
        cdf['trainer_code'] = self.df.trainer_code.str.strip()

        cdf['weight'] = self.df.horse_weight.astype(int)
        cdf['weight_diff'] = self.df.horse_weight_diff.str.replace(' ', '') \
            .apply(parse_int_or, args=(np.nan,)) \
            .astype('Int64')

        cdf['running_style'] = self.df.running_style_code.map(RUNNING_STYLE.get_key_map())
        cdf['pace_flow_id'] = PaceFlowCode.key2id(self.df.horse_pace_flow_code, allow_null=True)
        cdf['c4_race_line'] = self.df.c4_race_line.map(RACE_LINE.get_key_map())

        # disqualified contenders have blank purse;
        # but blank is equivalent to 0 in this case
        cdf['purse'] = self.df.purse.str.strip().where(lambda x: x != '', 0).astype(float)

        # Horse
        hdf = pd.DataFrame(index=rdf.index)
        hdf['pedigree_reg_num'] = self.df.pedigree_reg_num
        hdf['name'] = self.df.horse_name.str.strip()

        rdf.rename(columns=lambda col: 'race_' + str(col), inplace=True)
        cdf.rename(columns=lambda col: 'contender_' + str(col), inplace=True)
        hdf.rename(columns=lambda col: 'horse_' + str(col), inplace=True)

        return pd.concat([rdf, cdf, hdf], axis='columns')

    def persist(self):
        df = self.clean()

        for row in df.to_dict('records'):
            self._save_race_from_row_dict(row)
            self._save_horse_from_row_dict(row)
            self._save_contender_from_row_dict(row)

    def _save_race_from_row_dict(self, row: dict):
        prefix = 'race_'

        attrs = filter_na({
            key[len(prefix):]: val for key, val in row.items() if key.startswith(prefix)
        })

        try:
            Race.objects.create(**attrs)
        except IntegrityError:
            key = {
                'racetrack_id': attrs['racetrack_id'],
                'yr': attrs['yr'],
                'round': attrs['round'],
                'day': attrs['day'],
                'num': attrs['num']
            }

            Race.objects.filter(**key).update(**attrs)

    def _save_horse_from_row_dict(self, row: dict):
        prefix = 'horse_'

        attrs = filter_na({
            k[len(prefix):]: v for k, v in row.items() if k.startswith(prefix)
        })

        try:
            Horse.objects.create(**attrs)
        except IntegrityError:
            Horse.objects.filter(pedigree_reg_num=attrs['pedigree_reg_num']).update(**attrs)

    def _save_contender_from_row_dict(self, row: dict):
        prefix = 'contender_'

        attrs = filter_na({
            k[len(prefix):]: v for k, v in row.items() if k.startswith(prefix)
        })

        race_key = {
            'racetrack_id': row['race_racetrack_id'],
            'yr': row['race_yr'],
            'round': row['race_round'],
            'day': row['race_day'],
            'num': row['race_num']
        }

        race, _ = Race.objects.get_or_create(**race_key)
        horse, _ = Horse.objects.get_or_create(pedigree_reg_num=row['horse_pedigree_reg_num'])
        jockey, _ = Jockey.objects.get_or_create(code=attrs.pop('jockey_code'))
        trainer, _ = Trainer.objects.get_or_create(code=attrs.pop('trainer_code'))

        attrs['race_id'] = race.id
        attrs['horse_id'] = horse.id
        attrs['jockey_id'] = jockey.id
        attrs['trainer_id'] = trainer.id

        try:
            Contender.objects.create(**attrs)
        except IntegrityError:
            keys = ['race_id', 'horse_id', 'jockey_id', 'trainer_id']
            updates = {key: value for key, value in attrs.items() if key not in keys}
            Contender.objects.filter(race=race, horse=horse, jockey=jockey, trainer=trainer).update(**updates)
