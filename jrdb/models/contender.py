from django.db import models

from jrdb.models import choices


class Contender(models.Model):
    race = models.ForeignKey('jrdb.Race', models.CASCADE, verbose_name='レース')
    num = models.PositiveSmallIntegerField('馬番')

    horse = models.ForeignKey('jrdb.Horse', models.SET_NULL, verbose_name='馬', null=True)
    jockey = models.ForeignKey('jrdb.Jockey', models.SET_NULL, verbose_name='騎手', null=True)
    trainer = models.ForeignKey('jrdb.Trainer', models.SET_NULL, verbose_name='調教師', null=True)

    # SEDから取得（成績系）
    order_of_finish = models.PositiveSmallIntegerField('着順', null=True)
    penalty = models.CharField('異常区分', max_length=255, null=True, choices=choices.PENALTY.CHOICES())
    time = models.FloatField('タイム', null=True)
    mounted_weight = models.FloatField('斤量', null=True)
    odds_win = models.FloatField('確定単勝オッズ', null=True)
    odds_show = models.FloatField('確定複勝オッズ下', null=True)
    odds_win_10am = models.FloatField('10時単勝オッズ', null=True)
    odds_show_10am = models.FloatField('10時複勝オッズ', null=True)
    popularity = models.PositiveSmallIntegerField('確定単勝人気順位', null=True)

    idm = models.SmallIntegerField('ＩＤＭ', null=True)
    speed_idx = models.SmallIntegerField('素点', null=True)
    pace = models.SmallIntegerField('ペース', null=True)
    positioning = models.SmallIntegerField('位置取', null=True)
    late_start = models.PositiveSmallIntegerField('出遅', null=True)
    disadvt = models.PositiveSmallIntegerField('不利', null=True)
    b3f_disadvt = models.PositiveSmallIntegerField('前不利', null=True, help_text='前３Ｆ内での不利')
    mid_disadvt = models.PositiveSmallIntegerField('中不利', null=True, help_text='道中での不利')
    f3f_disadvt = models.PositiveSmallIntegerField('後不利', null=True, help_text='後３Ｆ内での不利')

    race_line = models.CharField('コース取り', max_length=255, choices=choices.RACE_LINE.CHOICES(), null=True)
    improvement = models.CharField('上昇度コード', max_length=255, choices=choices.IMPROVEMENT.CHOICES(), null=True)
    physique = models.CharField('馬体コード', max_length=255, choices=choices.PHYSIQUE.CHOICES(), null=True)
    demeanor = models.CharField('気配コード', max_length=255, choices=choices.DEMEANOR.CHOICES(), null=True)

    pace_cat = models.CharField('馬ペース', max_length=255, choices=choices.PACE_CATEGORY.CHOICES(), null=True)
    b3f_time_idx = models.FloatField('テン指数', null=True, help_text='前３Ｆタイムを指数化したもの')
    f3f_time_idx = models.FloatField('上がり指数', null=True, help_text='後３Ｆタイムを指数化したもの')
    pace_idx = models.FloatField('ペース指数', null=True, help_text='馬のペースを指数化したもの')
    margin = models.FloatField('1(2)着タイム差', null=True, help_text='0.1秒単位')
    b3f_time = models.FloatField('前３Ｆタイム', null=True, help_text='0.1秒単位')
    f3f_time = models.FloatField('後３Ｆタイム', null=True, help_text='0.1秒単位')

    c1p = models.PositiveSmallIntegerField('コーナー順位１', null=True)
    c2p = models.PositiveSmallIntegerField('コーナー順位２', null=True)
    c3p = models.PositiveSmallIntegerField('コーナー順位３', null=True)
    c4p = models.PositiveSmallIntegerField('コーナー順位４', null=True)

    b3f_1p_margin = models.FloatField('前３Ｆ先頭差', null=True, help_text='前３Ｆ地点での先頭とのタイム差（0.1秒単位）')
    f3f_1p_margin = models.FloatField('後３Ｆ先頭差', null=True, help_text='後３Ｆ地点での先頭とのタイム差（0.1秒単位）')

    weight = models.PositiveSmallIntegerField('馬体重', null=True)
    weight_diff = models.SmallIntegerField('馬体重増減', null=True)

    run_style = models.CharField('レース脚質', max_length=255, null=True, choices=choices.RUNNING_STYLE.CHOICES())
    purse = models.FloatField('本賞金', null=True)
    pace_flow = models.ForeignKey('jrdb.PaceFlowCode', models.CASCADE, verbose_name='本賞金', null=True)
    c4_race_line = models.CharField('４角コース取り', max_length=255, null=True, choices=choices.RACE_LINE.CHOICES(),
                                    help_text='1:最内,2:内,3:中,4:外,5:大外')

    # (KYI)
    weight_reduction = models.CharField('', max_length=255, null=True, choices=choices.WEIGHT_REDUCTION.CHOICES())
    prel_jockey_idx = models.FloatField('騎手指数', null=True, help_text='基準オッズと騎手の連対率の関係を基に算出された指数値')
    prel_info_idx = models.FloatField('情報指数', null=True, help_text='基準オッズ、厩舎指数、調教指数等様々な情報を基に算出された指数値')
    prel_total_idx = models.FloatField('総合指数', null=True, help_text='ＩＤＭ、騎手指数、情報指数を合計した値')
    prel_pop_idx = models.PositiveSmallIntegerField('人気指数', null=True, help_text='その馬の人気を指数化した値')
    prel_trainer_idx = models.FloatField('調教指数', null=True)
    prel_stable_idx = models.FloatField('厩舎指数', null=True)
    flat_out_run_idx = models.SmallIntegerField('激走指数', null=True)
    rotation = models.PositiveSmallIntegerField('ローテーション', null=True, help_text='間に金曜日が入っている数で決定、連闘は０、初出走はNULL')
    prel_idm = models.FloatField('前日ＩＤＭ', null=True)
    prel_run_style = models.CharField('前日脚質', max_length=255, null=True, choices=choices.RUNNING_STYLE.CHOICES())
    dist_apt = models.PositiveSmallIntegerField('距離適性', null=True)
    prel_improvement = models.CharField('前日上昇度コード', max_length=255, null=True, choices=choices.IMPROVEMENT.CHOICES())
    odds_win_base = models.FloatField('基準オッズ', null=True)
    pop_win_base = models.PositiveSmallIntegerField('基準人気順位', null=True)
    odds_show_base = models.FloatField('基準複勝オッズ', null=True)
    pop_show_base = models.PositiveSmallIntegerField('基準複勝人気順位', null=True)
    sym_sp_c_dbl = models.PositiveSmallIntegerField('特定情報◎', null=True)
    sym_sp_c = models.PositiveSmallIntegerField('特定情報○', null=True)
    sym_sp_t_dark = models.PositiveSmallIntegerField('特定情報▲', null=True)
    sym_sp_t = models.PositiveSmallIntegerField('特定情報△', null=True)
    sym_sp_x = models.PositiveSmallIntegerField('特定情報×', null=True)
    sym_total_c_dbl = models.PositiveSmallIntegerField('総合情報◎', null=True)
    sym_total_c = models.PositiveSmallIntegerField('総合情報○', null=True)
    sym_total_t_dark = models.PositiveSmallIntegerField('総合情報▲', null=True)
    sym_total_t = models.PositiveSmallIntegerField('総合情報△', null=True)
    sym_total_x = models.PositiveSmallIntegerField('総合情報×', null=True)
    trainer_outlook = models.CharField('調教矢印コード', max_length=255, null=True,
                                       choices=choices.TRAINER_HORSE_EVALUATION.CHOICES())
    stable_outlook = models.CharField('厩舎評価コード', max_length=255, null=True,
                                      choices=choices.STABLE_HORSE_EVALUATION.CHOICES())
    jockey_exp_1o2_place_rate = models.FloatField('騎手期待連対率', null=True,
                                                  help_text='騎手Ａが単勝基準オッズＢの馬に乗った場合の過去の成績を集計し、算出された連対率')
    paddock_observed_hoof = models.CharField('蹄コード', max_length=255, null=True,
                                             choices=choices.PADDOCK_OBSERVED_HOOF.CHOICES())
    yield_track_apt = models.CharField('重適正コード', max_length=255, null=True,
                                       choices=choices.YIELDING_TRACK_APTITUDE.CHOICES())
    blinker = models.CharField('ブリンカー', max_length=255, null=True, choices=choices.BLINKER.CHOICES())
    post_position = models.PositiveSmallIntegerField('枠番', null=True)

    # 印コード
    sym_overall = models.PositiveSmallIntegerField('総合印', null=True)
    sym_idm = models.PositiveSmallIntegerField('ＩＤＭ印', null=True)
    sym_info = models.PositiveSmallIntegerField('情報印', null=True)
    sym_jockey = models.PositiveSmallIntegerField('騎手印', null=True)
    sym_stable = models.PositiveSmallIntegerField('厩舎印', null=True)
    sym_trainer = models.PositiveSmallIntegerField('調教印', null=True)
    is_flat_out_runner = models.BooleanField('激走印', null=True)
    turf_apt = models.CharField('芝適性コード', max_length=255, null=True, choices=choices.APTITUDE_CODE.CHOICES())
    dirt_apt = models.CharField('ダ適性コード', max_length=255, null=True, choices=choices.APTITUDE_CODE.CHOICES())

    # 展開予想データ
    prel_b3f_time_idx = models.FloatField('予想テン指数', null=True)
    prel_pace_idx = models.FloatField('予想ペース指数', null=True)
    prel_f3f_time_idx = models.FloatField('予想上がり指数', null=True)
    prel_position_idx = models.FloatField('予想位置指数', null=True)
    prel_pace_cat = models.CharField('馬ペース', max_length=255, null=True, choices=choices.PACE_CATEGORY.CHOICES())
    mid_race_position = models.PositiveSmallIntegerField('道中順位', null=True)
    mid_race_margin = models.FloatField('道中差', null=True)
    mid_race_line = models.CharField('道中内外', max_length=255, null=True, choices=choices.RACE_LINE.CHOICES())
    f3f_position = models.PositiveSmallIntegerField('後３Ｆ順位', null=True)
    f3f_margin = models.FloatField('後３Ｆ差', null=True)
    f3f_race_line = models.CharField('後３Ｆ内外', max_length=255, null=True, choices=choices.RACE_LINE.CHOICES())
    goal_position = models.PositiveSmallIntegerField('ゴール順位', null=True)
    goal_margin = models.FloatField('ゴール差', null=True)
    goal_race_line = models.CharField('ゴール内外', max_length=255, null=True, choices=choices.RACE_LINE.CHOICES())
    race_development_symbol = models.CharField('展開記号', max_length=255, null=True,
                                               choices=choices.RACE_DEVELOPMENT_SYMBOL.CHOICES())

    dist_apt_2 = models.PositiveSmallIntegerField('距離適性２', null=True)
    # null is not an acceptable value for is_scratched, so do not use NullBooleanField
    # but may be missing during import, so setting null=True on BooleanField
    is_scratched = models.BooleanField('取消フラグ', null=True)
    flat_out_run_position = models.PositiveSmallIntegerField('激走順位', null=True, help_text='レース出走馬中での順位')
    ls_idx_position = models.PositiveSmallIntegerField('LS指数順位', null=True)
    b3f_idx_position = models.PositiveSmallIntegerField('テン指数順位', null=True)
    pace_idx_position = models.PositiveSmallIntegerField('ペース指数順位', null=True)
    f3f_idx_position = models.PositiveSmallIntegerField('上がり指数順位', null=True)
    positioning_idx_position = models.PositiveSmallIntegerField('位置指数順位', null=True)
    jockey_exp_win_rate = models.FloatField('騎手期待単勝率', null=True)
    jockey_exp_show_rate = models.FloatField('騎手期待３着内率', null=True)
    transport_category = models.CharField('輸送区分', max_length=255, null=True,
                                          choices=choices.TRANSPORT_CATEGORY.CHOICES())

    # 体型
    figure_overall = models.CharField('体型', max_length=255, null=True, choices=choices.FIGURE_OVERALL.CHOICES(),
                                      help_text='馬体の全体的な形状')
    length_back = models.CharField('背中', max_length=255, null=True, choices=choices.FIGURE_LENGTH.CHOICES())
    length_body = models.CharField('体型', max_length=255, null=True, choices=choices.FIGURE_LENGTH.CHOICES())
    size_rump = models.CharField('背中', max_length=255, null=True, choices=choices.FIGURE_SIZE.CHOICES())
    size_hindquarters = models.CharField('胴', max_length=255, null=True, choices=choices.FIGURE_ANGLE.CHOICES())
    size_belly = models.CharField('尻', max_length=255, null=True, choices=choices.FIGURE_SIZE.CHOICES())
    size_head = models.CharField('トモ', max_length=255, null=True, choices=choices.FIGURE_SIZE.CHOICES())
    length_neck = models.CharField('腹袋', max_length=255, null=True, choices=choices.FIGURE_LENGTH.CHOICES())
    size_breast = models.CharField('頭', max_length=255, null=True, choices=choices.FIGURE_SIZE.CHOICES())
    size_shoulder = models.CharField('首', max_length=255, null=True, choices=choices.FIGURE_ANGLE.CHOICES())
    length_front = models.CharField('前長', max_length=255, null=True, choices=choices.FIGURE_LENGTH.CHOICES())
    length_rear = models.CharField('後長', max_length=255, null=True, choices=choices.FIGURE_LENGTH.CHOICES())
    stride_front = models.CharField('前幅', max_length=255, null=True, choices=choices.FIGURE_STRIDE.CHOICES())
    stride_rear = models.CharField('後幅', max_length=255, null=True, choices=choices.FIGURE_STRIDE.CHOICES())
    length_pastern_front = models.CharField('前繋', max_length=255, null=True, choices=choices.FIGURE_LENGTH.CHOICES())
    length_pastern_rear = models.CharField('後繋', max_length=255, null=True, choices=choices.FIGURE_LENGTH.CHOICES())
    is_dock_raised = models.BooleanField('尾', null=True, help_text='つけ根の上げ方 TRUE:上げる, FALSE:下げる')
    tail_swing_intensity = models.CharField('振', max_length=255, null=True,
                                            choices=choices.TAIL_SWING_INTENSITY.CHOICES())

    figure_sp_mention_1 = models.ForeignKey('jrdb.SpecialMentionCode', models.SET_NULL, '+', verbose_name='体型総合１',
                                            null=True)
    figure_sp_mention_2 = models.ForeignKey('jrdb.SpecialMentionCode', models.SET_NULL, '+', verbose_name='体型総合２',
                                            null=True)
    figure_sp_mention_3 = models.ForeignKey('jrdb.SpecialMentionCode', models.SET_NULL, '+', verbose_name='体型総合３',
                                            null=True)
    horse_sp_mention_1 = models.ForeignKey('jrdb.SpecialMentionCode', models.SET_NULL, '+', verbose_name='馬特記１',
                                           null=True)
    horse_sp_mention_2 = models.ForeignKey('jrdb.SpecialMentionCode', models.SET_NULL, '+', verbose_name='馬特記２',
                                           null=True)
    horse_sp_mention_3 = models.ForeignKey('jrdb.SpecialMentionCode', models.SET_NULL, '+', verbose_name='馬特記３',
                                           null=True)

    # 展開参考データ
    horse_start_idx = models.FloatField('馬スタート指数', null=True)
    late_start_rate = models.FloatField('馬出遅率', null=True)

    big_bet_idx = models.PositiveSmallIntegerField('万券指数', null=True)
    sym_big_bet = models.PositiveSmallIntegerField('万券印', null=True)
    rank_lowered = models.CharField('降級フラグ', max_length=255, null=True, choices=choices.RANK_LOWERED.CHOICES())
    flat_out_run_type = models.CharField('激走タイプ', max_length=255, null=True,
                                         choices=choices.FLAT_OUT_RUN_TYPE.CHOICES())
    rest_reason = models.CharField('休養理由分類コード', max_length=255, null=True, choices=choices.REST_REASON.CHOICES())
    prior_context_surface = models.CharField('芝ダ障害フラグ', max_length=255, null=True,
                                             choices=choices.PRIOR_CONTEXT_SURFACE.CHOICES())
    is_longest_race_dist_yet = models.BooleanField('距離フラグ', null=True)
    prior_context_race_class = models.CharField('クラスフラグ', max_length=255, null=True,
                                                choices=choices.PRIOR_CONTEXT_RACE_CLASS.CHOICES())
    nth_race_since_stable_change = models.PositiveSmallIntegerField('転厩フラグ', null=True)
    nth_race_since_castration = models.PositiveSmallIntegerField('去勢フラグ', null=True)
    # ??? = ('乗替フラグ', max_length=255, null=True, choices=choices.???.CHOICES())
    nth_race_since_training_start = models.PositiveSmallIntegerField('入厩何走目', null=True)
    training_start_date = models.DateField('入厩年月日', null=True)
    nth_day_since_training_start = models.PositiveSmallIntegerField('入厩何日前', null=True)
    pasture_name = models.CharField('放牧先', max_length=255, null=True)
    pasture_rank = models.CharField('放牧先ランク', max_length=255, null=True, choices=choices.PASTURE_RANK.CHOICES())
    stable_rank = models.CharField('厩舎ランク', max_length=255, null=True, choices=choices.STABLE_RANK.CHOICES())

    # (SKB)
    sp_mention = models.ForeignKey('jrdb.SpecialMentionCode', models.SET_NULL, '+', verbose_name='特記コード', null=True)
    horse_gear = models.ForeignKey('jrdb.HorseGearCode', models.SET_NULL, '+', verbose_name='馬具コード', null=True)

    # 脚元コード
    hoof_overall = models.ForeignKey('jrdb.HorseGearCode', models.SET_NULL, '+', verbose_name='総合', null=True)
    hoof_front_left = models.ForeignKey('jrdb.HorseGearCode', models.SET_NULL, '+', verbose_name='左前', null=True)
    hoof_front_right = models.ForeignKey('jrdb.HorseGearCode', models.SET_NULL, '+', verbose_name='右前', null=True)
    hoof_back_left = models.ForeignKey('jrdb.HorseGearCode', models.SET_NULL, '+', verbose_name='左後', null=True)
    hoof_back_right = models.ForeignKey('jrdb.HorseGearCode', models.SET_NULL, '+', verbose_name='右後', null=True)

    paddock_comment = models.CharField('パドックコメント', max_length=40, null=True)
    hoof_comment = models.CharField('脚元コメント', max_length=40, null=True)
    horse_gear_or_other_comment = models.CharField('馬具', max_length=40, null=True)
    race_comment = models.CharField('レースコメント', max_length=40, null=True)

    # 分析用データ
    bit = models.ForeignKey('jrdb.HorseGearCode', models.SET_NULL, '+', verbose_name='ハミ', null=True)
    bandage = models.BooleanField('バンテージ', null=True)
    horseshoe = models.ForeignKey('jrdb.HorseGearCode', models.SET_NULL, '+', verbose_name='蹄鉄', null=True)
    hoof_cond = models.ForeignKey('jrdb.HorseGearCode', models.SET_NULL, '+', verbose_name='蹄状態', null=True)
    periostitis = models.ForeignKey('jrdb.HorseGearCode', models.SET_NULL, '+', verbose_name='ソエ', null=True)
    exostosis = models.ForeignKey('jrdb.HorseGearCode', models.SET_NULL, '+', verbose_name='骨瘤', null=True)

    # (CYB)
    training_style = models.CharField('調教タイプ', max_length=255, null=True, choices=choices.TRAINING_STYLE.CHOICES())
    training_course_cat = models.CharField('調教コース種別', max_length=255, null=True,
                                           choices=choices.TRAINING_COURSE_CATEGORY.CHOICES())
    trained_hill = models.BooleanField('坂', null=True, help_text='坂路')
    trained_wood_chip = models.BooleanField('Ｗ', null=True, help_text='ウッドコース')
    trained_dirt = models.BooleanField('ダ', null=True, help_text='ダートコース')
    trained_turf = models.BooleanField('芝', null=True, help_text='芝コース')
    trained_pool = models.BooleanField('プ', null=True, help_text='プール調教')
    trained_obstacle = models.BooleanField('障', null=True, help_text='障害練習')
    trained_poly_track = models.BooleanField('ポ', null=True, help_text='ポリトラック')
    training_distance = models.CharField('調教距離', max_length=255, null=True, choices=choices.TRAINING_DISTANCE.CHOICES())
    training_emphasis = models.CharField('調教重点', max_length=255, null=True, choices=choices.TRAINING_EMPHASIS.CHOICES())
    warm_up_time_idx = models.PositiveSmallIntegerField('追切指数', null=True)
    training_result_idx = models.PositiveSmallIntegerField('仕上指数', null=True)
    training_amount_eval = models.CharField('調教量評価', max_length=255, null=True,
                                            choices=choices.TRAINING_AMOUNT_EVAL.CHOICES())
    training_result_idx_change = models.CharField('仕上指数変化', max_length=255, null=True,
                                                  choices=choices.TRAINING_RESULT_IDX_CHANGE.CHOICES())
    training_comment = models.CharField('調教コメント', max_length=255, null=True)
    training_comment_date = models.DateField('コメント年月日', null=True)
    training_evaluation = models.CharField('調教評価', max_length=255, null=True,
                                           choices=choices.THREE_STAGE_EVAL.CHOICES())

    class Meta:
        db_table = 'contenders'
        unique_together = ('race', 'num')
