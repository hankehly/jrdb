import logging

import numpy as np
import pandas as pd
from django.db import IntegrityError, transaction

from ..models import RaceConditionCode, Jockey, PaceFlowCode, Racetrack, Trainer, Race, Contender, Horse, choices
from .parse import parse_int_or, parse_float_or, select_index_startwith
from .template import Template
from .item import StringItem, ForeignKeyItem, IntegerItem

logger = logging.getLogger(__name__)


class SED(Template):
    """
    http://www.jrdb.com/program/Sed/sed_doc.txt

    The "種別" values in the above document are incorrect.
    The correct values can be found [here](http://www.jrdb.com/program/jrdb_code.txt)
    """
    name = 'JRDB成績データ（SED）'

    items = [
        # レースキー
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Race.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Race.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Race.round'),
        StringItem('日', 1, 5, 'jrdb.Race.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        IntegerItem('馬番', 2, 8, 'jrdb.Contender.num'),
        StringItem('血統登録番号', 8, 10, 'jrdb.Horse.pedigree_reg_num'),
        # StringItem('race_date', '年月日', '8',  '19', 'YYYYMMDD <-暫定版より順序'),  # IGNORED (use value from BA),
        StringItem('馬名', 36, 26, 'jrdb.Horse.name'),

        # レース条件
        IntegerItem('距離', 4, 62, 'jrdb.Race.distance'),
        StringItem('芝ダ障害コード', 1, 66, 'jrdb.Race.surface_code'),
        StringItem('右左', 1, 67, 'jrdb.Race.direction'),
        StringItem('内外', 1, 68, 'jrdb.Race.course_inout'),
        StringItem('馬場状態', 2, 69, 'jrdb.Race.track_cond_code'),
        StringItem('種別', 2, 71, 'jrdb.Race.category_code'),
        StringItem('条件', 2, 73, 'jrdb.Race.cond_code'),
        StringItem('記号', 3, 75, 'jrdb.Race.symbols'),
        StringItem('重量', 1, 78, 'jrdb.Race.impost_class_code'),
        StringItem('グレード', 1, 79, 'jrdb.Race.grade'),
        StringItem('レース名', 50, 80, 'jrdb.Race.name'),
        StringItem('頭数', 2, 130, 'jrdb.Race.contender_count'),
        StringItem('レース名略称', 8, 132, 'jrdb.Race.name_abbr'),
        # 馬成績
        StringItem('着順', 2, 140, 'order_of_finish'),
        StringItem('異常区分', 1, 142, 'penalty_code'),
        StringItem('タイム', 4, 143, 'time'),
        StringItem('斤量', 3, 147, 'mounted_weight'),
        StringItem('騎手名', 12, 150, 'jockey_name'),
        StringItem('調教師名', 12, 162, 'trainer_name'),
        StringItem('確定単勝オッズ', 6, 174, 'fin_win_odds'),
        StringItem('確定単勝人気順位', 2, 180, 'fin_win_pop'),
        # ＪＲＤＢデータ
        StringItem('ＩＤＭ', 3, 182, 'IDM'),
        StringItem('素点', 3, 185, 'speed_idx'),
        StringItem('馬場差', 3, 188, 'track_speed_shift'),
        StringItem('ペース', 3, 191, 'pace'),
        StringItem('出遅', 3, 194, 'late_start'),
        StringItem('位置取', 3, 197, 'positioning'),
        StringItem('不利', 3, 200, 'disadvt'),
        StringItem('前不利', 3, 203, 'b3f_disadvt'),
        StringItem('中不利', 3, 206, 'mid_disadvt'),
        StringItem('後不利', 3, 209, 'f3f_disadvt'),
        # 単位/意味不明
        # StringItem('レース', 3, 212, 'race_ind'),  # IGNORED
        StringItem('コース取り', 1, 215, 'race_line'),
        StringItem('上昇度コード', 1, 216, 'improvement_code'),
        # TODO: Why does race_class_code differ between horses in the same race?
        # StringItem('クラスコード', 2, 217, 'race_class_code'),  # IGNORED
        StringItem('馬体コード', 1, 219, 'horse_physique_code'),
        StringItem('気配コード', 1, 220, 'horse_demeanor_code'),
        StringItem('レースペース', 1, 221, 'race_pace'),
        StringItem('馬ペース', 1, 222, 'horse_pace'),
        # テン指数はダッシュ力を意味する（元になる数値は前３Ｆタイム）
        StringItem('テン指数', 5, 223, 'b3f_time_idx'),
        # 勝負所からの最後の脚（元になる数値は後3Fタイム）
        StringItem('上がり指数', 5, 228, 'f3f_time_idx'),
        # ペース指数は道中どれぐらいのペースで後３Ｆを走ったか（元になる数値は走破タイム-後3Fタイム）
        StringItem('ペース指数', 5, 233, 'horse_pace_idx'),
        StringItem('レースＰ指数', 5, 238, 'race_pace_idx'),
        # for 1st place horses, the second place horse name/time
        # for 2nd > place horses, the first place horse name/time
        # StringItem('1(2)着馬名', 12, 243, 'fos_horse_name'),  # IGNORED
        StringItem('1(2)着タイム差', 3, 255, 'margin'),
        StringItem('前３Ｆタイム', 3, 258, 'b3f_time'),
        StringItem('後３Ｆタイム', 3, 261, 'f3f_time'),
        # StringItem('備考', 24, 264, 'note'),  # IGNORED
        StringItem('確定複勝オッズ下', 6, 290, 'fin_show_odds'),
        StringItem('10時単勝オッズ', 6, 296, 'odds_win_10AM'),
        StringItem('10時複勝オッズ', 6, 302, 'odds_show_10AM'),
        StringItem('コーナー順位１', 2, 308, 'c1p'),
        StringItem('コーナー順位２', 2, 310, 'c2p'),
        StringItem('コーナー順位３', 2, 312, 'c3p'),
        StringItem('コーナー順位４', 2, 314, 'c4p'),
        StringItem('前３Ｆ先頭差', 3, 316, 'b3f_1p_margin'),
        StringItem('後３Ｆ先頭差', 3, 319, 'f3f_1p_margin'),
        StringItem('騎手コード', 5, 322, 'jockey_code'),
        StringItem('調教師コード', 5, 327, 'trainer_code'),
        StringItem('馬体重', 3, 332, 'horse_weight'),
        StringItem('馬体重増減', 3, 335, 'horse_weight_diff'),
        StringItem('天候コード', 1, 338, 'weather_code'),
        StringItem('コース', 1, 339, 'course_label'),
        StringItem('レース脚質', 1, 340, 'running_style_code'),
        # StringItem('単勝', 7, 341, 'win_payoff_yen'),  # IGNORED
        # StringItem('複勝', 7, 348, 'show_payoff_yen'),  # IGNORED
        StringItem('本賞金', 5, 355, 'purse'),
        # StringItem('収得賞金', 5, 360, 'p1_prize'),  # IGNORED
        StringItem('レースペース流れ', 2, 365, 'race_pace_flow_code'),
        StringItem('馬ペース流れ', 2, 367, 'horse_pace_flow_code'),
        StringItem('４角コース取り', 1, 369, 'c4_race_line'),
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
        rdf['surface'] = self.df.race_surface_code.map(choices.SURFACE.get_key_map())
        rdf['direction'] = self.df.race_direction.map(choices.DIRECTION.get_key_map())
        rdf['course_inout'] = self.df.race_course_inout.map(choices.COURSE_INOUT.get_key_map())
        rdf['track_cond'] = self.df.race_track_cond_code.map(choices.TRACK_CONDITION.get_key_map())
        rdf['category'] = self.df.race_category_code.map(choices.RACE_CATEGORY.get_key_map())
        rdf['cond_id'] = RaceConditionCode.key2id(self.df.race_cond_code)
        rdf['horse_type_symbol'] = self.df.race_symbols.str[0].map(choices.RACE_HORSE_TYPE_SYMBOL.get_key_map())
        rdf['horse_sex_symbol'] = self.df.race_symbols.str[1].map(choices.RACE_HORSE_SEX_SYMBOL.get_key_map())
        rdf['interleague_symbol'] = self.df.race_symbols.str[2].map(choices.RACE_INTERLEAGUE_SYMBOL.get_key_map())
        rdf['impost_class'] = self.df.race_impost_class_code.map(choices.IMPOST_CLASS.get_key_map())
        rdf['grade'] = self.df.race_grade.map(choices.GRADE.get_key_map())
        rdf['name'] = self.df.race_name.str.strip()
        rdf['name_abbr'] = self.df.race_name_abbr.str.strip()
        rdf['track_speed_shift'] = self.df.track_speed_shift.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        rdf['pace_cat'] = self.df.race_pace.map(choices.PACE_CATEGORY.get_key_map())
        rdf['pace_idx'] = self.df.race_pace_idx.apply(parse_float_or, args=(np.nan,))
        rdf['weather'] = self.df.weather_code.map(choices.WEATHER.get_key_map())
        rdf['course_label'] = self.df.course_label.map(choices.COURSE_LABEL.get_key_map())
        rdf['pace_flow_id'] = PaceFlowCode.key2id(self.df.race_pace_flow_code, allow_null=True)

        # Contender
        cdf = pd.DataFrame(index=rdf.index)
        cdf['num'] = self.df.horse_num.astype(int)
        cdf['order_of_finish'] = self.df.order_of_finish.astype(int)
        cdf['penalty'] = self.df.penalty_code.map(choices.PENALTY.get_key_map())
        cdf['time'] = self.df.time.apply(parse_float_or, args=(np.nan,)) * 0.1
        cdf['mounted_weight'] = self.df.mounted_weight.astype(int) * 0.1
        cdf['odds_win'] = self.df.fin_win_odds.apply(parse_float_or, args=(np.nan,))
        cdf['popularity'] = self.df.fin_win_pop.astype(int)
        cdf['IDM'] = self.df.IDM.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['speed_idx'] = self.df.speed_idx.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['pace'] = self.df.pace.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['positioning'] = self.df.positioning.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['disadvt'] = self.df.disadvt.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['late_start'] = self.df.late_start.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['b3f_disadvt'] = self.df.b3f_disadvt.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['mid_disadvt'] = self.df.mid_disadvt.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['f3f_disadvt'] = self.df.f3f_disadvt.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['race_line'] = self.df.race_line.map(choices.RACE_LINE.get_key_map())
        cdf['improvement'] = self.df.improvement_code.map(choices.IMPROVEMENT.get_key_map())
        cdf['physique'] = self.df.horse_physique_code.map(choices.PHYSIQUE.get_key_map())
        cdf['demeanor'] = self.df.horse_demeanor_code.map(choices.DEMEANOR.get_key_map())
        cdf['pace_cat'] = self.df.horse_pace.map(choices.PACE_CATEGORY.get_key_map())
        cdf['b3f_time_idx'] = self.df.b3f_time_idx.apply(parse_float_or, args=(np.nan,))
        cdf['f3f_time_idx'] = self.df.f3f_time_idx.apply(parse_float_or, args=(np.nan,))
        cdf['pace_idx'] = self.df.horse_pace_idx.apply(parse_float_or, args=(np.nan,))
        cdf['margin'] = self.df.margin.apply(parse_float_or, args=(np.nan,)) * 0.1
        cdf['b3f_time'] = self.df.b3f_time.apply(parse_float_or, args=(np.nan,)) * 0.1
        cdf['f3f_time'] = self.df.f3f_time.apply(parse_float_or, args=(np.nan,)) * 0.1
        cdf['odds_show'] = self.df.odds_show.apply(parse_float_or, args=(np.nan,))
        cdf['odds_win_10AM'] = self.df.odds_win_10AM.apply(parse_float_or, args=(np.nan,))
        cdf['odds_show_10AM'] = self.df.odds_show_10AM.apply(parse_float_or, args=(np.nan,))
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

        cdf['running_style'] = self.df.running_style_code.map(choices.RUNNING_STYLE.get_key_map())
        cdf['pace_flow_id'] = PaceFlowCode.key2id(self.df.horse_pace_flow_code, allow_null=True)
        cdf['c4_race_line'] = self.df.c4_race_line.map(choices.RACE_LINE.get_key_map())

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

    @transaction.atomic
    def persist(self):
        for _, row in self.clean().iterrows():
            r = row.pipe(select_index_startwith, 'race__', rename=True).dropna().to_dict()
            race, _ = Race.objects.get_or_create(racetrack_id=r.pop('racetrack_id'), yr=r.pop('yr'),
                                                 round=r.pop('round'), day=r.pop('day'), num=r.pop('num'))

            h = row.pipe(select_index_startwith, 'horse__', rename=True).dropna().to_dict()
            horse, _ = Horse.objects.get_or_create(pedigree_reg_num=h.pop('pedigree_reg_num'), defaults=h)

            j = row.pipe(select_index_startwith, 'jockey__', rename=True).dropna().to_dict()
            jockey, _ = Jockey.objects.get_or_create(code=j.pop('code'), defaults=j)

            t = row.pipe(select_index_startwith, 'trainer__', rename=True).dropna().to_dict()
            trainer, _ = Trainer.objects.get_or_create(code=t.pop('code'), defaults=t)

            try:
                c = row.pipe(select_index_startwith, 'contender__', rename=True).dropna().to_dict()
                Contender.objects.update_or_create(race=race, horse=horse, jockey=jockey, trainer=trainer, defaults=c)
            except IntegrityError as e:
                logger.exception(e)
