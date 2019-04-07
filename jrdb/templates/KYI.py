import numpy as np
import pandas as pd

from jrdb.templates.template import Template
from jrdb.models import choices, Racetrack, Race, Contender, Horse, Jockey, Trainer
from jrdb.templates.parse import parse_int_or, parse_float_or


class KYI(Template):
    """
    http://www.jrdb.com/program/Kyi/kyi_doc.txt
    http://www.jrdb.com/program/Kyi/ky_siyo_doc.txt
    """
    name = 'JRDB競走馬データ（KYI）'
    items = [
        # レースキー
        [Race.racetrack, '場コード', None, '2', '99', '1', None],
        [Race.yr, '年', None, '2', '99', '3', None],
        [Race.round, '回', None, '1', '9', '5', None],
        [Race.day, '日', None, '1', 'F', '6', '16進数(数字 or 小文字アルファベット)'],
        [Race.num, 'Ｒ', None, '2', '99', '7', None],
        [Contender.num, '馬番', None, '2', '99', '9', None],
        [Horse.pedigree_reg_num, '血統登録番号', None, '8', 'X', '11', None],
        [Horse.name, '馬名', None, '36', 'X', '19', '全角１８文字'],

        [Contender.prel_IDM, 'ＩＤＭ', None, '5', 'ZZ9.9', '55', None],
        [Contender.prel_jockey_idx, '騎手指数', None, '5', 'ZZ9.9', '60', None],
        [Contender.prel_info_idx, '情報指数', None, '5', 'ZZ9.9', '65', None],
        ['', '予備１', None, '5', 'ZZ9.9', '70', '将来拡張用'],
        ['', '予備２', None, '5', 'ZZ9.9', '75', '将来拡張用'],
        ['', '予備３', None, '5', 'ZZ9.9', '80', '将来拡張用'],
        [Contender.prel_total_idx, '総合指数', None, '5', 'ZZ9.9', '85', None],

        [Contender.prel_run_style, '脚質', None, '1', '9', '90', None],
        [Contender.dist_apt, '距離適性', None, '1', '9', '91', None],
        [Contender.prel_improvement, '上昇度', None, '1', '9', '92', None],
        [Contender.rotation, 'ローテーション', None, '3', 'ZZ9', '93', '間に金曜日が入っている数で決定、連闘は０、初出走はスペースとなる'],

        [Contender.odds_win_base, '基準オッズ', None, '5', 'ZZ9.9', '96', None],
        [Contender.pop_win_base, '基準人気順位', None, '2', 'Z9', '101', None],
        [Contender.odds_show, '基準複勝オッズ', None, '5', 'ZZ9.9', '103', None],
        [Contender.pop_show_base, '基準複勝人気順位', None, '2', 'Z9', '108', None],
        [Contender.sym_sp_c_dbl, '特定情報◎', None, '3', 'ZZ9', '110', '情報・専門紙の印数（特定）'],
        [Contender.sym_sp_c, '特定情報○', None, '3', 'ZZ9', '113', None],
        [Contender.sym_sp_t_dark, '特定情報▲', None, '3', 'ZZ9', '116', None],
        [Contender.sym_sp_t, '特定情報△', None, '3', 'ZZ9', '119', None],
        [Contender.sym_sp_x, '特定情報×', None, '3', 'ZZ9', '122', None],
        [Contender.sym_total_c_dbl, '総合情報◎', None, '3', 'ZZ9', '125', '情報・専門紙の印数（総合）'],
        [Contender.sym_total_c, '総合情報○', None, '3', 'ZZ9', '128', None],
        [Contender.sym_total_t_dark, '総合情報▲', None, '3', 'ZZ9', '131', None],
        [Contender.sym_total_t, '総合情報△', None, '3', 'ZZ9', '134', None],
        [Contender.sym_total_x, '総合情報×', None, '3', 'ZZ9', '137', None],
        [Contender.prel_pop_idx, '人気指数', None, '5', 'ZZZZ9', '140', '第２版で変更'],
        [Contender.prel_trainer_idx, '調教指数', None, '5', 'ZZ9.9', '145', None],
        [Contender.prel_stable_idx, '厩舎指数', None, '5', 'ZZ9.9', '150', None],
        # ===以下第３版にて追加===
        [Contender.trainer_outlook, '調教矢印コード', None, '1', '9', '155', None],
        [Contender.stable_outlook, '厩舎評価コード', None, '1', '9', '156', None],
        # 騎手Ａが単勝基準オッズＢの馬に乗った場合の過去の成績を集計し、算出された連対率を騎手期待連対率としています。
        [Contender.jockey_exp_1o2_place_rate, '騎手期待連対率', None, '4', 'Z9.9', '157', None],
        # ＪＲＤＢでの穴馬分析は激走指数
        [Contender.flat_out_run_idx, '激走指数', None, '3', 'ZZ9', '161', None],
        [Contender.paddock_observed_hoof, '蹄コード', None, '2', '99', '164', None],
        [Contender.yield_track_apt, '重適性コード', None, '1', '9', '166', None],
        ['race_class', 'クラスコード', None, '2', '99', '167', None],  # why is each horse different? IGNORED
        ['', '予備', None, '2', 'X', '169', 'スペース'],
        # ===以下第４版にて追加===
        [Contender.blinker, 'ブリンカー', None, '1', 'X', '171', '1:初装着,2:再装着,3:ブリンカ'],
        [Jockey.name, '騎手名', None, '12', 'X', '172', '全角６文字'],
        [Contender.mounted_weight, '負担重量', None, '3', '999', '184', '0.1Kg単位'],
        [Jockey.trainee_cat, '見習い区分', None, '1', '9', '187', '1:☆(1K減),2:△(2K減),3:▲(3K減)'],
        [Trainer.name, '調教師名', None, '12', 'X', '188', '全角６文字'],
        [Trainer.area, '調教師所属', None, '4', 'X', '200', '全角２文字'],
        # 他データリンク用キー
        ['', '前走１競走成績キー', None, '16', '9', '204', None],  # IGNORED
        ['', '前走２競走成績キー', None, '16', '9', '220', None],  # IGNORED
        ['', '前走３競走成績キー', None, '16', '9', '236', None],  # IGNORED
        ['', '前走４競走成績キー', None, '16', '9', '252', None],  # IGNORED
        ['', '前走５競走成績キー', None, '16', '9', '268', None],  # IGNORED
        ['', '前走１レースキー', None, '8', '9', '284', None],  # IGNORED
        ['', '前走２レースキー', None, '8', '9', '292', None],  # IGNORED
        ['', '前走３レースキー', None, '8', '9', '300', None],  # IGNORED
        ['', '前走４レースキー', None, '8', '9', '308', None],  # IGNORED
        ['', '前走５レースキー', None, '8', '9', '316', None],  # IGNORED
        [Contender.post_position, '枠番', None, '1', '9', '324', None],
        ['', '予備', None, '2', 'X', '325', 'スペース'],
        # ===以下第５版にて追加===
        # 印コード
        # [Contender.sym_overall, '総合印', None, '1', '9', '327', '印コード'],
        # [Contender.sym_IDM, 'ＩＤＭ印', None, '1', '9', '328', '印コード'],
        # [Contender.sym_info, '情報印', None, '1', '9', '329', '印コード'],
        # [Contender.sym_jockey, '騎手印', None, '1', '9', '330', '印コード'],
        # [Contender.sym_stable, '厩舎印', None, '1', '9', '331', '印コード'],
        # [Contender.sym_trainer, '調教印', None, '1', '9', '332', '印コード'],
        # [Contender.is_flat_out_runner, '激走印', None, '1', '9', '333', '1:激走馬'],
        #
        # [Contender.turf_apt, '芝適性コード', None, '1', 'X', '334', '1:◎, 2:○, 3:△'],
        # [Contender.dirt_apt, 'ダ適性コード', None, '1', 'X', '335', '1:◎, 2:○, 3:△'],
        [Jockey.code, '騎手コード', None, '5', '9', '336', '騎手マスタとリンク'],
        [Trainer.code, '調教師コード', None, '5', '9', '341', '調教師マスタとリンク'],
        ['', '予備', None, '1', 'X', '346', 'スペース'],
        # ===以下第６版にて追加===
        # 賞金情報
        ['', '獲得賞金', None, '6', 'ZZZZZ9', '347', '単位万円(含む付加賞)'],
        ['p1_prize', '収得賞金', None, '5', 'ZZZZ9', '353', '単位万円'],  # IGNORED
        ['race_condition_group_code', '条件クラス', None, '1', '9', '358', '条件グループコード参照\n収得賞金から出走できるクラス'],  # IGNORED

        # 展開予想データ
        [Contender.prel_b3f_time_idx, 'テン指数', None, '5', 'ZZZ.9', '359', '予想テン指数'],
        [Contender.prel_pace_idx, 'ペース指数', None, '5', 'ZZZ.9', '364', '予想ペース指数'],
        [Contender.prel_f3f_time_idx, '上がり指数', None, '5', 'ZZZ.9', '369', '予想上がり指数'],
        [Contender.prel_position_idx, '位置指数', None, '5', 'ZZZ.9', '374', '予想位置指数'],
        [Contender.prel_pace_cat, 'ペース予想', None, '1', 'X', '379', 'H,M,S'],
        ['mid_race_position', '道中順位', None, '2', 'Z9', '380', None],
        ['mid_race_margin', '道中差', None, '2', 'Z9', '382', '半馬身(約0.1秒)単位'],
        ['mid_race_in_out', '道中内外', None, '1', '9', '384', '2:内 ～ 4:外'],
        ['f3f_position', '後３Ｆ順位', None, '2', 'Z9', '385', None],
        ['f3f_margin', '後３Ｆ差', None, '2', 'Z9', '387', '半馬身(約0.1秒)単位'],
        ['f3f_in_out', '後３Ｆ内外', None, '1', '9', '389', '2:内 ～ 5:大外'],
        ['goal_position', 'ゴール順位', None, '2', 'Z9', '390', None],
        ['goal_margin', 'ゴール差', None, '2', 'Z9', '392', '半馬身(約0.1秒)単位'],
        ['goal_in_out', 'ゴール内外', None, '1', '9', '394', '1:最内 ～ 5:大外'],
        ['race_development_symbol', '展開記号', None, '1', 'X', '395', '展開記号コード参照'],
        # ===以下第６a版にて追加===
        ['dist_apt_2', '距離適性２', None, '1', '9', '396', None],  # 意味不明
        ['weight_pp_decision', '枠確定馬体重', None, '3', '999', '397', 'データ無:スペース'],
        ['weight_diff_pp_decision', '枠確定馬体重増減', None, '3', 'XZ9', '400', '符号+数字２桁,データ無:スペース'],
        # ===以下第７版にて追加===
        ['is_cancelled', '取消フラグ', None, '1', '9', '403', '1:取消'],
        [Horse.sex, '性別コード', None, '1', '9', '404', '1:牡,2:牝,3,セン'],
        [Horse.owner_name, '馬主名', None, '40', 'X', '405', '全角２０文字'],
        [Horse.owner_racetrack, '馬主会コード', None, '2', '99', '445', '参考データ。'],
        [Horse.symbol, '馬記号コード', None, '2', '99', '447', 'コード表参照'],
        ['flat_out_run_position', '激走順位', None, '2', 'Z9', '449', 'レース出走馬中での順位'],
        ['LS_idx_position', 'LS指数順位', None, '2', 'Z9', '451', None],
        ['b3f_idx_position', 'テン指数順位', None, '2', 'Z9', '453', None],
        ['pace_idx_position', 'ペース指数順位', None, '2', 'Z9', '455', None],
        ['f3f_idx_position', '上がり指数順位', None, '2', 'Z9', '457', None],
        ['positioning_idx_position', '位置指数順位', None, '2', 'Z9', '459', None],
        # ===以下第８版にて追加===
        ['jockey_exp_win_rate', '騎手期待単勝率', None, '4', 'Z9.9', '461', None],
        ['jockey_exp_show_rate', '騎手期待３着内率', None, '4', 'Z9.9', '465', None],
        ['transport_category', '輸送区分', None, '1', 'X', '469', None],
        # ===以下第９版にて追加===
        ['', '走法', None, '8', '9', '470', 'コード表参照'],  # IGNORED (走法データの採取は休止)
        ['figure', '体型', None, '24', 'X', '478', 'コード表参照'],
        ['figure_overall_1', '体型総合１', None, '3', '9', '502', '特記コード参照'],  # sp_mention_code
        ['figure_overall_2', '体型総合２', None, '3', '9', '505', '特記コード参照'],
        ['figure_overall_3', '体型総合３', None, '3', '9', '508', '特記コード参照'],
        ['horse_sp_mention_1', '馬特記１', None, '3', '9', '511', '特記コード参照'],
        ['horse_sp_mention_2', '馬特記２', None, '3', '9', '514', '特記コード参照'],
        ['horse_sp_mention_3', '馬特記３', None, '3', '9', '517', '特記コード参照'],
        # 展開参考データ
        ['horse_start_idx', '馬スタート指数', None, '4', 'Z9.9', '520', None],
        ['late_start_rate', '馬出遅率', None, '4', 'Z9.9', '524', None],
        ['', '参考前走', None, '2', '99', '528', '参考となる前走（２走分格納）'],  # 1, 2, 3など（意味不明）
        ['', '参考前走騎手コード', None, '5', 'X', '530', '参考となる前走の騎手'],  # 同上
        ['big_bet_idx', '万券指数', None, '3', 'ZZ9', '535', None],
        ['big_bet_symbol', '万券印', None, '1', '9', '538', None],
        # ===以下第10版にて追加===
        ['rank_lowered', '降級フラグ', None, '1', '9', '539', '1:降級, 2:２段階降級, 0:通常'],
        ['flat_out_run_type', '激走タイプ', None, '2', 'XX', '540', '激走馬のタイプ分け。説明参照'],
        ['rest_reason_code', '休養理由分類コード', None, '2', '99', '542', 'コード表参照'],
        # ===以下第11版にて追加===
        ['flags', 'フラグ', None, '16', 'X', '544', '初芝初ダ初障などのフラグ'],
        ['nth_race_since_training_start', '入厩何走目', None, '2', 'Z9', '560', '例）2:入厩後２走目'],
        ['training_start_date', '入厩年月日', None, '8', '9', '562', 'YYYYMMDD'],
        ['nth_day_since_training_start', '入厩何日前', None, '3', 'ZZ9', '570', 'レース日から遡っての入厩の日数'],
        ['pasture_name', '放牧先', None, '50', 'X', '573', '放牧先/近走放牧先'],
        ['pasture_rank', '放牧先ランク', None, '1', 'X', '623', 'A-E'],
        ['stable_rank', '厩舎ランク', None, '1', '9', '624', '高い1-9低い 内容説明参照'],
        ['', '予備', None, '398', 'X', '625', 'スペース'],
        ['', '改行', None, '2', 'X', '1023', 'ＣＲ・ＬＦ']
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
