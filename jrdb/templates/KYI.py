import numpy as np
import pandas as pd

from ..models import choices, Racetrack, Contender, Horse, Jockey, Trainer
from .item import ForeignKeyItem, IntegerItem, StringItem, FloatItem, ChoiceItem
from .parse import parse_int_or, parse_float_or
from .template import Template


class KYI(Template):
    """
    http://www.jrdb.com/program/Kyi/kyi_doc.txt
    http://www.jrdb.com/program/Kyi/ky_siyo_doc.txt
    """
    name = 'JRDB競走馬データ（KYI）'
    items = [
        # レースキー
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Race.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Race.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Race.round'),
        StringItem('日', 1, 5, 'jrdb.Race.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        IntegerItem('馬番', 2, 8, 'jrdb.Contender.num'),
        IntegerItem('血統登録番号', 8, 10, 'jrdb.Horse.pedigree_reg_num'),
        IntegerItem('馬名', 36, 18, 'jrdb.Horse.name'),

        FloatItem('ＩＤＭ', 5, 54, 'jrdb.Contender.prel_IDM'),
        FloatItem('騎手指数', 5, 59, 'jrdb.Contender.prel_jockey_idx'),
        FloatItem('情報指数', 5, 64, 'jrdb.Contender.prel_info_idx'),
        FloatItem('総合指数', 5, 84, 'jrdb.Contender.prel_total_idx'),

        ChoiceItem('脚質', 1, 89, 'jrdb.Contender.prel_run_style', options=choices.RUNNING_STYLE.options()),
        IntegerItem('距離適性', 1, 90, 'jrdb.Contender.dist_apt'),
        ChoiceItem('上昇度', 1, 91, 'jrdb.Contender.prel_improvement', options=choices.IMPROVEMENT.options()),
        IntegerItem('ローテーション', 3, 92, 'jrdb.Contender.rotation'),

        FloatItem('基準オッズ', 5, 95, 'jrdb.Contender.odds_win_base'),
        IntegerItem('基準人気順位', 2, 100, 'jrdb.Contender.pop_win_base'),
        FloatItem('基準複勝オッズ', 5, 102, 'jrdb.Contender.odds_show'),
        IntegerItem('基準複勝人気順位', 2, 107, 'jrdb.Contender.pop_show_base'),
        IntegerItem('特定情報◎', 3, 109, 'jrdb.Contender.sym_sp_c_dbl'),
        IntegerItem('特定情報○', 3, 112, 'jrdb.Contender.sym_sp_c'),
        IntegerItem('特定情報▲', 3, 115, 'jrdb.Contender.sym_sp_t_dark'),
        IntegerItem('特定情報△', 3, 118, 'jrdb.Contender.sym_sp_t'),
        IntegerItem('特定情報×', 3, 121, 'jrdb.Contender.sym_sp_x'),
        IntegerItem('総合情報◎', 3, 124, 'jrdb.Contender.sym_total_c_dbl'),
        IntegerItem('総合情報○', 3, 127, 'jrdb.Contender.sym_total_c'),
        IntegerItem('総合情報▲', 3, 130, 'jrdb.Contender.sym_total_t_dark'),
        IntegerItem('総合情報△', 3, 133, 'jrdb.Contender.sym_total_t'),
        IntegerItem('総合情報×', 3, 136, 'jrdb.Contender.sym_total_x'),
        IntegerItem('人気指数', 5, 139, 'jrdb.Contender.prel_pop_idx'),
        FloatItem('調教指数', 5, 144, 'jrdb.Contender.prel_trainer_idx'),
        FloatItem('厩舎指数', 5, 149, 'jrdb.Contender.prel_stable_idx'),
        # ===以下第３版にて追加===
        IntegerItem('調教矢印コード', 1, 154, 'jrdb.Contender.trainer_outlook'),
        IntegerItem('厩舎評価コード', 1, 155, 'jrdb.Contender.stable_outlook'),
        # 騎手Ａが単勝基準オッズＢの馬に乗った場合の過去の成績を集計し、算出された連対率を騎手期待連対率としています。
        FloatItem('騎手期待連対率', 4, 156, 'jrdb.Contender.jockey_exp_1o2_place_rate'),
        # ＪＲＤＢでの穴馬分析は激走指数
        IntegerItem('激走指数', 3, 160, 'jrdb.Contender.flat_out_run_idx'),
        ChoiceItem('蹄コード', 2, 163, 'jrdb.Contender.paddock_observed_hoof',
                   options=choices.PADDOCK_OBSERVED_HOOF.options()),
        IntegerItem('重適性コード', 1, 165, 'jrdb.Contender.yield_track_apt'),
        # TODO: why is each horse different? IGNORE
        # IntegerItem('jrdb.race_class', 'クラスコード', '2', '99', '167'),
        # ===以下第４版にて追加===
        ChoiceItem('ブリンカー', 1, 170, 'jrdb.Contender.blinker', options=choices.BLINKER.options()),
        StringItem('騎手名', 12, 171, 'jrdb.Jockey.name'),
        FloatItem('負担重量', 3, 183, 'jrdb.Contender.mounted_weight'),
        ChoiceItem('見習い区分', 1, 186, 'jrdb.Jockey.trainee_cat', options=choices.TRAINEE_CATEGORY.options()),
        StringItem('調教師名', 12, 187, 'jrdb.Trainer.name'),
        ChoiceItem('調教師所属', 4, 199, 'jrdb.Trainer.area', options=choices.AREA.options()),
        # 他データリンク用キー
        # '前走１競走成績キー', '16', '204'  # IGNORE
        # '前走２競走成績キー', '16', '220'  # IGNORE
        # '前走３競走成績キー', '16', '236'  # IGNORE
        # '前走４競走成績キー', '16', '252'  # IGNORE
        # '前走５競走成績キー', '16', '268'  # IGNORE
        # '前走１レースキー', '8', '284'  # IGNORE
        # '前走２レースキー', '8', '292'  # IGNORE
        # '前走３レースキー', '8', '300'  # IGNORE
        # '前走４レースキー', '8', '308'  # IGNORE
        # '前走５レースキー', '8', '316'  # IGNORE
        IntegerItem('枠番', 1, 323, 'jrdb.Contender.post_position'),
        # ===以下第５版にて追加===
        # 印コード
        # IntegerItem(jrdb.Contender.sym_overall, '総合印', '1', '327', '印コード'),
        # IntegerItem(jrdb.Contender.sym_IDM, 'ＩＤＭ印', '1', '328', '印コード'),
        # IntegerItem(jrdb.Contender.sym_info, '情報印', '1', '329', '印コード'),
        # IntegerItem(jrdb.Contender.sym_jockey, '騎手印', '1', '330', '印コード'),
        # IntegerItem(jrdb.Contender.sym_stable, '厩舎印', '1', '331', '印コード'),
        # IntegerItem(jrdb.Contender.sym_trainer, '調教印', '1', '332', '印コード'),
        # IntegerItem(jrdb.Contender.is_flat_out_runner, '激走印', '1', '333', '1:激走馬'),
        #
        # IntegerItem(jrdb.Contender.turf_apt, '芝適性コード', '1', '334', '1:◎, 2:○, 3:△'),
        # IntegerItem(jrdb.Contender.dirt_apt, 'ダ適性コード', '1', '335', '1:◎, 2:○, 3:△'),
        ForeignKeyItem('騎手コード', 5, 335, 'jrdb.Contender.jockey', 'jrdb.Jockey.code'),
        ForeignKeyItem('調教師コード', 5, 340, 'jrdb.Contender.trainer', 'jrdb.Trainer.code'),
        # ===以下第６版にて追加===
        # 賞金情報
        # IntegerItem('jrdb.', '獲得賞金', '6', 'ZZZZZ9', '347', '単位万円(含む付加賞)'),
        # IntegerItem('jrdb.p1_prize', '収得賞金', '5', '353', '単位万円'),  # IGNORE
        # IntegerItem('jrdb.race_condition_group_code', '条件クラス', '1', '358', '条件グループコード参照\n収得賞金から出走できるクラス'),  # IGNORE

        # 展開予想データ
        FloatItem('テン指数', 5, 358, 'jrdb.Contender.prel_b3f_time_idx'),
        FloatItem('ペース指数', 5, 363, 'jrdb.Contender.prel_pace_idx'),
        FloatItem('上がり指数', 5, 368, 'jrdb.Contender.prel_f3f_time_idx'),
        FloatItem('位置指数', 5, 373, 'jrdb.Contender.prel_position_idx'),
        ChoiceItem('ペース予想', 1, 378, 'jrdb.Contender.prel_pace_cat', choices.PACE_CATEGORY.options()),
        IntegerItem('jrdb.mid_race_position', '道中順位', '2', '380'),
        IntegerItem('jrdb.mid_race_margin', '道中差', '2', '382', '半馬身(約0.1秒)単位'),
        IntegerItem('jrdb.mid_race_in_out', '道中内外', '1', '384', '2:内 ～ 4:外'),
        IntegerItem('jrdb.f3f_position', '後３Ｆ順位', '2', '385'),
        IntegerItem('jrdb.f3f_margin', '後３Ｆ差', '2', '387', '半馬身(約0.1秒)単位'),
        IntegerItem('jrdb.f3f_in_out', '後３Ｆ内外', '1', '389', '2:内 ～ 5:大外'),
        IntegerItem('jrdb.goal_position', 'ゴール順位', '2', '390'),
        IntegerItem('jrdb.goal_margin', 'ゴール差', '2', '392', '半馬身(約0.1秒)単位'),
        IntegerItem('jrdb.goal_in_out', 'ゴール内外', '1', '394', '1:最内 ～ 5:大外'),
        IntegerItem('jrdb.race_development_symbol', '展開記号', '1', '395', '展開記号コード参照'),
        # ===以下第６a版にて追加===
        IntegerItem('jrdb.dist_apt_2', '距離適性２', '1', '396'),  # 意味),
        IntegerItem('jrdb.weight_pp_decision', '枠確定馬体重', '3', '397', 'データ無:スペース'),
        IntegerItem('jrdb.weight_diff_pp_decision', '枠確定馬体重増減', '3', 'XZ9', '400', '符号+数字２桁,データ無:スペース'),
        # ===以下第７版にて追加===
        IntegerItem('jrdb.is_cancelled', '取消フラグ', '1', '403', '1:取消'),
        IntegerItem(jrdb.Horse.sex, '性別コード', '1', '404', '1:牡,2:牝,3,セン'),
        IntegerItem(jrdb.Horse.owner_name, '馬主名', '40', '405', '全角２０文字'),
        IntegerItem(jrdb.Horse.owner_racetrack, '馬主会コード', '2', '99', '445', '参考データ。'),
        IntegerItem(jrdb.Horse.symbol, '馬記号コード', '2', '99', '447', 'コード表参照'),
        IntegerItem('jrdb.flat_out_run_position', '激走順位', '2', '449', 'レース出走馬中での順位'),
        IntegerItem('jrdb.LS_idx_position', 'LS指数順位', '2', '451'),
        IntegerItem('jrdb.b3f_idx_position', 'テン指数順位', '2', '453'),
        IntegerItem('jrdb.pace_idx_position', 'ペース指数順位', '2', '455'),
        IntegerItem('jrdb.f3f_idx_position', '上がり指数順位', '2', '457'),
        IntegerItem('jrdb.positioning_idx_position', '位置指数順位', '2', '459'),
        # ===以下第８版にて追加===
        IntegerItem('jrdb.jockey_exp_win_rate', '騎手期待単勝率', '4', '461'),
        IntegerItem('jrdb.jockey_exp_show_rate', '騎手期待３着内率', '4', '465'),
        IntegerItem('jrdb.transport_category', '輸送区分', '1', '469'),
        # ===以下第９版にて追加===
        IntegerItem('jrdb.', '走法', '8', '470', 'コード表参照'),  # IGNORED (走法データの採取は休),
        IntegerItem('jrdb.figure', '体型', '24', '478', 'コード表参照'),
        IntegerItem('jrdb.figure_overall_1', '体型総合１', '3', '502', '特記コード参照'),  # sp_mention_co),
        IntegerItem('jrdb.figure_overall_2', '体型総合２', '3', '505', '特記コード参照'),
        IntegerItem('jrdb.figure_overall_3', '体型総合３', '3', '508', '特記コード参照'),
        IntegerItem('jrdb.horse_sp_mention_1', '馬特記１', '3', '511', '特記コード参照'),
        IntegerItem('jrdb.horse_sp_mention_2', '馬特記２', '3', '514', '特記コード参照'),
        IntegerItem('jrdb.horse_sp_mention_3', '馬特記３', '3', '517', '特記コード参照'),
        # 展開参考データ
        IntegerItem('jrdb.horse_start_idx', '馬スタート指数', '4', '520'),
        IntegerItem('jrdb.late_start_rate', '馬出遅率', '4', '524'),
        IntegerItem('jrdb.', '参考前走', '2', '99', '528', '参考となる前走（２走分格納）'),  # 1, 2, 3など（意味不),
        IntegerItem('jrdb.', '参考前走騎手コード', '5', '530', '参考となる前走の騎手'),  # ),
        IntegerItem('jrdb.big_bet_idx', '万券指数', '3', '535'),
        IntegerItem('jrdb.big_bet_symbol', '万券印', '1', '538'),
        # ===以下第10版にて追加===
        IntegerItem('jrdb.rank_lowered', '降級フラグ', '1', '539', '1:降級, 2:２段階降級, 0:通常'),
        IntegerItem('jrdb.flat_out_run_type', '激走タイプ', '2', 'XX', '540', '激走馬のタイプ分け。説明参照'),
        IntegerItem('jrdb.rest_reason_code', '休養理由分類コード', '2', '99', '542', 'コード表参照'),
        # ===以下第11版にて追加===
        IntegerItem('jrdb.flags', 'フラグ', '16', '544', '初芝初ダ初障などのフラグ'),
        IntegerItem('jrdb.nth_race_since_training_start', '入厩何走目', '2', '560', '例）2:入厩後２走目'),
        IntegerItem('jrdb.training_start_date', '入厩年月日', '8', '562', 'YYYYMMDD'),
        IntegerItem('jrdb.nth_day_since_training_start', '入厩何日前', '3', '570', 'レース日から遡っての入厩の日数'),
        IntegerItem('jrdb.pasture_name', '放牧先', '50', '573', '放牧先/近走放牧先'),
        IntegerItem('jrdb.pasture_rank', '放牧先ランク', '1', '623', 'A-E'),
        IntegerItem('jrdb.stable_rank', '厩舎ランク', '1', '624', '高い1-9低い 内容説明参照'),
    ]

    def clean(self) -> pd.DataFrame:
        for column in self.df:
            pass

        # Race._meta.get_field('yr').get_internal_type()
        # 'PositiveSmallIntegerField'

        racetracks = Racetrack.objects.filter(code__in=self.df.racetrack_code).values('code', 'id')
        s = self.df.racetrack_code.map({racetrack['code']: racetrack['id'] for racetrack in racetracks})
        s.name = 'racetrack_id'

        rdf = s.to_frame()
        rdf['yr'] = self.df.yr.astype(int)
        rdf['round'] = self.df['round'].astype(int)
        rdf['day'] = self.df.day.str.strip()
        rdf['num'] = self.df.race_num.astype(int)

        cdf = pd.DataFrame(index=rdf.index)
        cdf['num'] = self.df.horse_num.astype(int)
        cdf['prel_jockey_idx'] = self.df.jockey_idx.apply(parse_float_or, args=(np.nan,))
        cdf['prel_info_idx'] = self.df.prel_info_idx.apply(parse_float_or, args=(np.nan,))
        cdf['prel_total_idx'] = self.df.prel_total_idx.apply(parse_float_or, args=(np.nan,))
        cdf['prel_pop_idx'] = self.df.prel_pop_idx.astype(int)
        cdf['prel_trainer_idx'] = self.df.prel_trainer_idx.apply(parse_float_or, args=(np.nan,))
        cdf['prel_stable_idx'] = self.df.prel_stable_idx.apply(parse_float_or, args=(np.nan,))
        cdf['flat_out_run_idx'] = self.df.flat_out_run_idx.astype(int)
        cdf['rotation'] = self.df.rotation.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['prel_IDM'] = self.df.prel_IDM.apply(parse_float_or, args=(np.nan,))
        cdf['prel_run_style'] = self.df.prel_run_style.map(choices.RUNNING_STYLE.get_key_map())
        cdf['dist_apt'] = self.df.dist_apt.astype(int)
        cdf['prel_improvement'] = self.df.prel_improvement.map(choices.IMPROVEMENT.get_key_map())
        cdf['odds_win_base'] = self.df.odds_win_base.apply(parse_float_or, args=(np.nan,))
        cdf['pop_win_base'] = self.df.pop_win_base.astype(int)
        cdf['odds_show_base'] = self.df.odds_show_base.apply(parse_float_or, args=(np.nan,))
        cdf['pop_show_base'] = self.df.pop_show_base.astype(int)
        cdf['sym_sp_c_dbl'] = self.df.sym_sp_c_dbl.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_sp_c'] = self.df.sym_sp_c.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_sp_t_dark'] = self.df.sym_sp_t_dark.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_sp_t'] = self.df.sym_sp_t.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_sp_x'] = self.df.sym_sp_x.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_total_c_dbl'] = self.df.sym_total_c_dbl.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_total_c'] = self.df.sym_total_c.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_total_t_dark'] = self.df.sym_total_t_dark.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_total_t'] = self.df.sym_total_t.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_total_x'] = self.df.sym_total_x.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['trainer_outlook'] = self.df.trainer_outlook.astype(int)
        cdf['stable_outlook'] = self.df.stable_outlook.astype(int)
        cdf['jockey_exp_1o2_place_rate'] = self.df.jockey_exp_1o2_place_rate.astype(float)
        cdf['paddock_observed_hoof'] = self.df.paddock_observed_hoof.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['yield_track_apt'] = self.df.yield_track_apt.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['blinker'] = self.df.blinker.map(choices.BLINKER.get_key_map())
        cdf['mounted_weight'] = self.df.mounted_weight.astype(int) * 0.1
        cdf['post_position'] = self.df.post_position.astype(int)
        cdf['sym_overall'] = self.df.sym_overall.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_IDM'] = self.df.sym_IDM.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_info'] = self.df.sym_info.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_jockey'] = self.df.sym_jockey.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_stable'] = self.df.sym_stable.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['sym_trainer'] = self.df.sym_trainer.apply(parse_int_or, args=(np.nan,)).astype('Int64')
        cdf['is_flat_out_runner'] = self.df.is_flat_out_runner.str.strip().astype(bool)
        cdf['turf_apt'] = self.df.turf_apt.map(choices.APTITUDE_CODE.get_key_map())
        cdf['dirt_apt'] = self.df.dirt_apt.map(choices.APTITUDE_CODE.get_key_map())
        cdf['prel_b3f_time_idx'] = self.df.prel_b3f_time_idx.apply(parse_float_or, args=(np.nan,))
        cdf['prel_pace_idx'] = self.df.prel_pace_idx.apply(parse_float_or, args=(np.nan,))
        cdf['prel_f3f_time_idx'] = self.df.prel_f3f_time_idx.apply(parse_float_or, args=(np.nan,))
        cdf['prel_pace_cat'] = self.df.prel_pace_cat.map(choices.PACE_CATEGORY.get_key_map())

        # Horse
        hdf = pd.DataFrame(index=rdf.index)
        hdf['pedigree_reg_num'] = self.df.pedigree_reg_num
        hdf['name'] = self.df.horse_name.str.strip()

        # Trainer
        tdf = pd.DataFrame(index=rdf.index)
        tdf['trainee_cat'] = self.df.trainee_cat.map(choices.TRAINEE_CATEGORY.get_key_map())
        tdf['name'] = self.df.trainer_name.str.strip()
        tdf['area'] = self.df.trainer_area.map(choices.AREA.get_key_map())
        tdf['code'] = self.df.trainer_code.str.strip()

        # Jockey
        jdf = pd.DataFrame(index=rdf.index)
        jdf['name'] = self.df.jockey_name.str.strip()
        jdf['code'] = self.df.jockey_code.str.strip()

        rdf.rename(columns=lambda col: 'race_' + str(col), inplace=True)
        cdf.rename(columns=lambda col: 'contender_' + str(col), inplace=True)
        hdf.rename(columns=lambda col: 'horse_' + str(col), inplace=True)
        tdf.rename(columns=lambda col: 'trainer_' + str(col), inplace=True)
        jdf.rename(columns=lambda col: 'jockey_' + str(col), inplace=True)

        return pd.concat([rdf, cdf, hdf, tdf, jdf], axis='columns')
