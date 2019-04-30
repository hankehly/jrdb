import logging

from ..models import choices
from .item import ForeignKeyItem, IntegerItem, StringItem, FloatItem, ChoiceItem, BooleanItem, DateItem
from .template import Template, startswith, DjangoUpsertMixin

logger = logging.getLogger(__name__)


class KYI(Template, DjangoUpsertMixin):
    """
    http://www.jrdb.com/program/Kyi/kyi_doc.txt
    http://www.jrdb.com/program/Kyi/ky_siyo_doc.txt
    """
    name = 'JRDB競走馬データ（KYI）'
    items = [
        # レースキー
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Program.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Program.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Program.round'),
        StringItem('日', 1, 5, 'jrdb.Program.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        IntegerItem('馬番', 2, 8, 'jrdb.Contender.num'),
        StringItem('血統登録番号', 8, 10, 'jrdb.Horse.pedigree_reg_num'),
        StringItem('馬名', 36, 18, 'jrdb.Horse.name'),

        FloatItem('ＩＤＭ', 5, 54, 'jrdb.Contender.prel_idm'),
        FloatItem('騎手指数', 5, 59, 'jrdb.Contender.prel_jockey_idx'),
        FloatItem('情報指数', 5, 64, 'jrdb.Contender.prel_info_idx'),
        FloatItem('総合指数', 5, 84, 'jrdb.Contender.prel_total_idx'),

        ChoiceItem('脚質', 1, 89, 'jrdb.Contender.prel_run_style', choices.RUNNING_STYLE.options()),
        IntegerItem('距離適性', 1, 90, 'jrdb.Contender.dist_apt'),
        ChoiceItem('上昇度', 1, 91, 'jrdb.Contender.prel_improvement', choices.IMPROVEMENT.options()),
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
        StringItem('調教矢印コード', 1, 154, 'jrdb.Contender.trainer_outlook'),
        StringItem('厩舎評価コード', 1, 155, 'jrdb.Contender.stable_outlook'),
        # 騎手Ａが単勝基準オッズＢの馬に乗った場合の過去の成績を集計し、算出された連対率を騎手期待連対率としています。
        FloatItem('騎手期待連対率', 4, 156, 'jrdb.Contender.jockey_exp_1o2_place_rate'),
        # ＪＲＤＢでの穴馬分析は激走指数
        IntegerItem('激走指数', 3, 160, 'jrdb.Contender.flat_out_run_idx'),
        ChoiceItem('蹄コード', 2, 163, 'jrdb.Contender.paddock_observed_hoof', choices.PADDOCK_OBSERVED_HOOF.options()),
        StringItem('重適性コード', 1, 165, 'jrdb.Contender.yield_track_apt'),
        # TODO: why is each horse different? IGNORE
        # IntegerItem('jrdb.race_class', 'クラスコード', 2, '99', '167'),
        # ===以下第４版にて追加===
        ChoiceItem('ブリンカー', 1, 170, 'jrdb.Contender.blinker', choices.BLINKER.options()),
        StringItem('騎手名', 12, 171, 'jrdb.Jockey.name'),
        FloatItem('負担重量', 3, 183, 'jrdb.Contender.mounted_weight'),
        ChoiceItem('見習い区分', 1, 186, 'jrdb.Contender.weight_reduction', choices.WEIGHT_REDUCTION.options()),
        StringItem('調教師名', 12, 187, 'jrdb.Trainer.name'),
        ChoiceItem('調教師所属', 4, 199, 'jrdb.Trainer.area', choices.AREA.options()),
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
        IntegerItem('総合印', 1, 326, 'jrdb.Contender.sym_overall'),
        IntegerItem('ＩＤＭ印', 1, 327, 'jrdb.Contender.sym_idm'),
        IntegerItem('情報印', 1, 328, 'jrdb.Contender.sym_info'),
        IntegerItem('騎手印', 1, 329, 'jrdb.Contender.sym_jockey'),
        IntegerItem('厩舎印', 1, 330, 'jrdb.Contender.sym_stable'),
        IntegerItem('調教印', 1, 331, 'jrdb.Contender.sym_trainer'),
        BooleanItem('激走印', 1, 332, 'jrdb.Contender.is_flat_out_runner'),

        ChoiceItem('芝適性コード', 1, 333, 'jrdb.Contender.turf_apt', choices.APTITUDE_CODE.options()),
        ChoiceItem('ダ適性コード', 1, 334, 'jrdb.Contender.dirt_apt', choices.APTITUDE_CODE.options()),
        StringItem('騎手コード', 5, 335, 'jrdb.Jockey.code'),
        StringItem('調教師コード', 5, 340, 'jrdb.Trainer.code'),
        # ===以下第６版にて追加===
        # 賞金情報
        # IntegerItem('jrdb.', '獲得賞金', '6', 'ZZZZZ9', '347', '単位万円(含む付加賞)'),
        # IntegerItem('jrdb.p1_prize', '収得賞金', 5, '353', '単位万円'),  # IGNORE
        # IntegerItem('jrdb.race_condition_group_code', '条件クラス', 1, '358', '条件グループコード参照\n収得賞金から出走できるクラス'),  # IGNORE

        # 展開予想データ
        FloatItem('テン指数', 5, 358, 'jrdb.Contender.prel_b3f_time_idx'),
        FloatItem('ペース指数', 5, 363, 'jrdb.Contender.prel_pace_idx'),
        FloatItem('上がり指数', 5, 368, 'jrdb.Contender.prel_f3f_time_idx'),
        FloatItem('位置指数', 5, 373, 'jrdb.Contender.prel_position_idx'),
        ChoiceItem('ペース予想', 1, 378, 'jrdb.Contender.prel_pace_cat', choices.PACE_CATEGORY.options()),
        IntegerItem('道中順位', 2, 379, 'jrdb.Contender.mid_race_position'),
        FloatItem('道中差', 2, 381, 'jrdb.Contender.mid_race_margin', scale=0.1),
        ChoiceItem('道中内外', 1, 383, 'jrdb.Contender.mid_race_line', choices.RACE_LINE.options()),
        IntegerItem('後３Ｆ順位', 2, 384, 'jrdb.Contender.f3f_position'),
        FloatItem('後３Ｆ差', 2, 386, 'jrdb.Contender.f3f_margin', scale=0.1),
        ChoiceItem('後３Ｆ内外', 1, 388, 'jrdb.Contender.f3f_race_line', choices.RACE_LINE.options()),
        IntegerItem('ゴール順位', 2, 389, 'jrdb.Contender.goal_position'),
        FloatItem('ゴール差', 2, 391, 'jrdb.Contender.goal_margin', scale=0.1),
        ChoiceItem('ゴール内外', 1, 393, 'jrdb.Contender.goal_race_line', choices.RACE_LINE.options()),
        ChoiceItem('展開記号', 1, 394, 'jrdb.Contender.race_development_symbol', choices.RACE_DEVELOPMENT_SYMBOL.options()),

        # ===以下第６a版にて追加===
        IntegerItem('距離適性２', 1, 395, 'jrdb.Contender.dist_apt_2'),
        # StringItem('枠確定馬体重', 3, 396, 'jrdb.Contender.post_position_decision_time_weight'), # データ無
        # StringItem('枠確定馬体重増減', 3, 399, 'jrdb.Contender.post_position_decision_time_weight_diff'), # データ無
        # ===以下第７版にて追加===
        BooleanItem('取消フラグ', 1, 402, 'jrdb.Contender.is_cancelled', value_false=''),
        StringItem('性別コード', 1, 403, 'jrdb.Horse.sex'),
        StringItem('馬主名', 40, 404, 'jrdb.Horse.owner_name'),
        ForeignKeyItem('馬主会コード', 2, 444, 'jrdb.Horse.owner_racetrack', 'jrdb.Racetrack.code'),
        ChoiceItem('馬記号コード', 2, 446, 'jrdb.Horse.symbol', choices.HORSE_SYMBOL.options()),
        IntegerItem('激走順位', 2, 448, 'jrdb.Contender.flat_out_run_position'),
        IntegerItem('LS指数順位', 2, 450, 'jrdb.Contender.ls_idx_position'),
        IntegerItem('テン指数順位', 2, 452, 'jrdb.Contender.b3f_idx_position'),
        IntegerItem('ペース指数順位', 2, 454, 'jrdb.Contender.pace_idx_position'),
        IntegerItem('上がり指数順位', 2, 456, 'jrdb.Contender.f3f_idx_position'),
        IntegerItem('位置指数順位', 2, 458, 'jrdb.Contender.positioning_idx_position'),
        # ===以下第８版にて追加===
        FloatItem('騎手期待単勝率', 4, 460, 'jrdb.Contender.jockey_exp_win_rate'),
        FloatItem('騎手期待３着内率', 4, 464, 'jrdb.Contender.jockey_exp_show_rate'),
        ChoiceItem('輸送区分', 1, 468, 'jrdb.Contender.transport_category', choices.TRANSPORT_CATEGORY.options()),
        # ===以下第９版にて追加===
        # StringItem('jrdb.', '走法', 8, 469, 'コード表参照'),  # IGNORED (走法データの採取は休),
        ChoiceItem('体型', 1, 477, 'jrdb.Contender.figure_overall', choices.FIGURE_OVERALL.options()),
        ChoiceItem('背中', 1, 478, 'jrdb.Contender.length_back', choices.FIGURE_LENGTH.options()),
        ChoiceItem('胴', 1, 479, 'jrdb.Contender.length_body', choices.FIGURE_LENGTH.options()),
        ChoiceItem('尻', 1, 480, 'jrdb.Contender.size_rump', choices.FIGURE_SIZE.options()),
        # ANGLEとSIZEは区別しなくていいのでは。。
        ChoiceItem('トモ', 1, 481, 'jrdb.Contender.size_hindquarters', choices.FIGURE_ANGLE.options()),
        ChoiceItem('腹袋', 1, 482, 'jrdb.Contender.size_belly', choices.FIGURE_SIZE.options()),
        ChoiceItem('頭', 1, 483, 'jrdb.Contender.size_head', choices.FIGURE_SIZE.options()),
        ChoiceItem('首', 1, 484, 'jrdb.Contender.length_neck', choices.FIGURE_LENGTH.options()),
        ChoiceItem('胸', 1, 485, 'jrdb.Contender.size_breast', choices.FIGURE_SIZE.options()),
        ChoiceItem('肩', 1, 486, 'jrdb.Contender.size_shoulder', choices.FIGURE_ANGLE.options()),
        ChoiceItem('前長', 1, 487, 'jrdb.Contender.length_front', choices.FIGURE_LENGTH.options()),
        ChoiceItem('後長', 1, 488, 'jrdb.Contender.length_rear', choices.FIGURE_LENGTH.options()),
        ChoiceItem('前幅', 1, 489, 'jrdb.Contender.stride_front', choices.FIGURE_STRIDE.options()),
        ChoiceItem('後幅', 1, 490, 'jrdb.Contender.stride_rear', choices.FIGURE_STRIDE.options()),
        ChoiceItem('前繋', 1, 491, 'jrdb.Contender.length_pastern_front', choices.FIGURE_LENGTH.options()),
        ChoiceItem('後繋', 1, 492, 'jrdb.Contender.length_pastern_rear', choices.FIGURE_LENGTH.options()),
        BooleanItem('尾', 1, 493, 'jrdb.Contender.is_dock_raised', value_false='2'),
        ChoiceItem('振', 1, 494, 'jrdb.Contender.tail_swing_intensity', choices.TAIL_SWING_INTENSITY.options()),
        ForeignKeyItem('体型総合１', 3, 501, 'jrdb.Contender.figure_sp_mention_1', 'jrdb.SpecialMentionCode.key'),
        ForeignKeyItem('体型総合２', 3, 504, 'jrdb.Contender.figure_sp_mention_2', 'jrdb.SpecialMentionCode.key'),
        ForeignKeyItem('体型総合３', 3, 507, 'jrdb.Contender.figure_sp_mention_3', 'jrdb.SpecialMentionCode.key'),
        ForeignKeyItem('馬特記１', 3, 510, 'jrdb.Contender.horse_sp_mention_1', 'jrdb.SpecialMentionCode.key'),
        ForeignKeyItem('馬特記２', 3, 513, 'jrdb.Contender.horse_sp_mention_2', 'jrdb.SpecialMentionCode.key'),
        ForeignKeyItem('馬特記３', 3, 516, 'jrdb.Contender.horse_sp_mention_3', 'jrdb.SpecialMentionCode.key'),
        # 展開参考データ
        FloatItem('馬スタート指数', 4, 519, 'jrdb.Contender.horse_start_idx'),
        FloatItem('馬出遅率', 4, 523, 'jrdb.Contender.late_start_rate'),
        # StringItem('jrdb.', '参考前走', 2, '99', '528', '参考となる前走（２走分格納）'),  # 1, 2, 3など（意味不),
        # StringItem('jrdb.', '参考前走騎手コード', 5, '530', '参考となる前走の騎手'),  # ),
        IntegerItem('万券指数', 3, 534, 'jrdb.Contender.big_bet_idx'),
        IntegerItem('万券印', 1, 537, 'jrdb.Contender.sym_big_bet'),
        # ===以下第10版にて追加===
        ChoiceItem('降級フラグ', 1, 538, 'jrdb.Contender.rank_lowered', choices.RANK_LOWERED.options()),
        ChoiceItem('激走タイプ', 2, 539, 'jrdb.Contender.flat_out_run_type', choices.FLAT_OUT_RUN_TYPE.options()),
        ChoiceItem('休養理由分類コード', 2, 541, 'jrdb.Contender.rest_reason', choices.REST_REASON.options()),
        # ===以下第11版にて追加===
        ChoiceItem('芝ダ障害フラグ', 1, 543, 'jrdb.Contender.prior_context_surface', choices.PRIOR_CONTEXT_SURFACE.options()),
        BooleanItem('距離フラグ', 1, 544, 'jrdb.Contender.is_longest_race_dist_yet'),
        ChoiceItem('クラスフラグ', 1, 545, 'jrdb.Contender.prior_context_race_class',
                   choices.PRIOR_CONTEXT_RACE_CLASS.options()),
        IntegerItem('転厩フラグ', 1, 546, 'jrdb.Contender.nth_race_since_stable_change'),
        IntegerItem('去勢フラグ', 1, 547, 'jrdb.Contender.nth_race_since_castration'),
        # ChoiceItem('乗替フラグ', 1, 548, 'jrdb.Contender.???'), # jockey change?
        IntegerItem('入厩何走目', 2, 559, 'jrdb.Contender.nth_race_since_training_start'),
        DateItem('入厩年月日', 8, 561, 'jrdb.Contender.training_start_date'),
        IntegerItem('入厩何日前', 3, 569, 'jrdb.Contender.nth_day_since_training_start'),
        StringItem('放牧先', 50, 572, 'jrdb.Contender.pasture_name'),
        ChoiceItem('放牧先ランク', 1, 622, 'jrdb.Contender.pasture_rank', choices.PASTURE_RANK.options()),
        ChoiceItem('厩舎ランク', 1, 623, 'jrdb.Contender.stable_rank', choices.STABLE_RANK.options()),
    ]

    def load(self):
        pdf = self.transform.pipe(startswith, 'program__', rename=True)
        programs = self.upsert('jrdb.Program').to_dataframe()
        program_id = pdf.merge(programs, how='left').id

        races = self.upsert('jrdb.Race', program_id=program_id).to_dataframe()
        rdf = self.transform.pipe(startswith, 'race__', rename=True)

        horses = self.upsert('jrdb.Horse').to_dataframe()
        hdf = self.transform.pipe(startswith, 'horse__', rename=True)

        jockeys = self.upsert('jrdb.Jockey').to_dataframe()
        jdf = self.transform.pipe(startswith, 'jockey__', rename=True)

        trainers = self.upsert('jrdb.Trainer').to_dataframe()
        tdf = self.transform.pipe(startswith, 'trainer__', rename=True)

        rdf['program_id'] = program_id
        race_id = rdf[['program_id', 'num']].merge(races, how='left').id
        horse_id = hdf.merge(horses, how='left').id
        jockey_id = jdf.merge(jockeys, how='left').id
        trainer_id = tdf.merge(trainers, how='left').id

        self.upsert('jrdb.Contender', race_id=race_id, horse_id=horse_id, jockey_id=jockey_id, trainer_id=trainer_id)
