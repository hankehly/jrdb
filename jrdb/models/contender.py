from django.db import models

from jrdb.models import BaseModel, choices


class Contender(BaseModel):
    race = models.ForeignKey('jrdb.Race', on_delete=models.CASCADE)
    horse = models.ForeignKey('jrdb.Horse', on_delete=models.CASCADE)
    jockey = models.ForeignKey('jrdb.Jockey', on_delete=models.CASCADE)
    trainer = models.ForeignKey('jrdb.Trainer', on_delete=models.CASCADE)
    num = models.PositiveSmallIntegerField(verbose_name='馬番')

    # SEDから取得（成績系）
    order_of_finish = models.PositiveSmallIntegerField(verbose_name='着順')
    penalty = models.CharField(max_length=255, verbose_name='異常区分', choices=choices.PENALTY.CHOICES())
    time = models.FloatField(null=True, verbose_name='タイム')
    mounted_weight = models.FloatField(verbose_name='斤量')
    odds_win = models.FloatField(null=True, verbose_name='確定単勝オッズ')
    odds_show = models.FloatField(null=True, verbose_name='確定複勝オッズ下')
    odds_win_10AM = models.FloatField(null=True, verbose_name='10時単勝オッズ')
    odds_show_10AM = models.FloatField(null=True, verbose_name='10時複勝オッズ')
    pop = models.PositiveSmallIntegerField(verbose_name='確定単勝人気順位')

    IDM = models.SmallIntegerField(null=True, verbose_name='ＩＤＭ')
    speed_idx = models.SmallIntegerField(null=True, verbose_name='素点')
    pace = models.SmallIntegerField(null=True, verbose_name='ペース')
    positioning = models.SmallIntegerField(null=True, verbose_name='位置取')
    late_start = models.PositiveSmallIntegerField(null=True, verbose_name='出遅')
    disadvt = models.PositiveSmallIntegerField(null=True, verbose_name='不利')
    b3f_disadvt = models.PositiveSmallIntegerField(null=True, verbose_name='前不利', help_text='前３Ｆ内での不利')
    mid_disadvt = models.PositiveSmallIntegerField(null=True, verbose_name='中不利', help_text='道中での不利')
    f3f_disadvt = models.PositiveSmallIntegerField(null=True, verbose_name='後不利', help_text='後３Ｆ内での不利')

    race_line = models.CharField(max_length=255, choices=choices.RACE_LINE.CHOICES(), verbose_name='コース取り')
    improvement = models.CharField(max_length=255, choices=choices.IMPROVEMENT.CHOICES(), verbose_name='上昇度コード')
    physique = models.CharField(max_length=255, choices=choices.PHYSIQUE.CHOICES(), verbose_name='馬体コード')
    demeanor = models.CharField(max_length=255, choices=choices.DEMEANOR.CHOICES(), verbose_name='気配コード')

    pace_cat = models.CharField(max_length=255, choices=choices.PACE_CATEGORY.CHOICES(), verbose_name='馬ペース')
    b3f_time_idx = models.FloatField(null=True, verbose_name='テン指数', help_text='前３Ｆタイムを指数化したもの')
    f3f_time_idx = models.FloatField(null=True, verbose_name='上がり指数', help_text='後３Ｆタイムを指数化したもの')
    pace_idx = models.FloatField(null=True, verbose_name='ペース指数', help_text='馬のペースを指数化したもの')
    margin = models.FloatField(null=True, verbose_name='1(2)着タイム差', help_text='0.1秒単位')
    b3f_time = models.FloatField(null=True, verbose_name='前３Ｆタイム', help_text='0.1秒単位')
    f3f_time = models.FloatField(null=True, verbose_name='後３Ｆタイム', help_text='0.1秒単位')

    c1p = models.PositiveSmallIntegerField(null=True, verbose_name='コーナー順位１')
    c2p = models.PositiveSmallIntegerField(null=True, verbose_name='コーナー順位２')
    c3p = models.PositiveSmallIntegerField(null=True, verbose_name='コーナー順位３')
    c4p = models.PositiveSmallIntegerField(null=True, verbose_name='コーナー順位４')

    b3f_1p_margin = models.FloatField(null=True, verbose_name='前３Ｆ先頭差', help_text='前３Ｆ地点での先頭とのタイム差（0.1秒単位）')
    f3f_1p_margin = models.FloatField(null=True, verbose_name='後３Ｆ先頭差', help_text='後３Ｆ地点での先頭とのタイム差（0.1秒単位）')

    weight = models.PositiveSmallIntegerField(verbose_name='馬体重')
    weight_diff = models.SmallIntegerField(null=True, verbose_name='馬体重増減')

    run_style = models.CharField(max_length=255, choices=choices.RUNNING_STYLE.CHOICES(), verbose_name='レース脚質')
    purse = models.FloatField()
    pace_flow = models.ForeignKey('jrdb.PaceFlowCode', null=True, on_delete=models.CASCADE, verbose_name='本賞金')
    c4_race_line = models.CharField(max_length=255, choices=choices.RACE_LINE.CHOICES(), verbose_name='４角コース取り',
                                    help_text='1:最内,2:内,3:中,4:外,5:大外')

    # KYIから取得（前日系）
    prel_jockey_idx = models.FloatField(verbose_name='騎手指数', help_text='基準オッズと騎手の連対率の関係を基に算出された指数値')
    prel_info_idx = models.FloatField(verbose_name='情報指数', help_text='基準オッズ、厩舎指数、調教指数等様々な情報を基に算出された指数値')
    prel_total_idx = models.FloatField(verbose_name='総合指数', help_text='ＩＤＭ、騎手指数、情報指数を合計した値')
    prel_pop_idx = models.PositiveSmallIntegerField(null=True, verbose_name='人気指数', help_text='その馬の人気を指数化した値')
    prel_trainer_idx = models.FloatField(verbose_name='調教指数')
    prel_stable_idx = models.FloatField(verbose_name='厩舎指数')
    flat_out_run_idx = models.SmallIntegerField(verbose_name='激走指数')
    rotation = models.PositiveSmallIntegerField(null=True, verbose_name='ローテーション',
                                                help_text='間に金曜日が入っている数で決定、連闘は０、初出走はNULL')
    prel_IDM = models.FloatField(null=True, verbose_name='前日ＩＤＭ')
    prel_run_style = models.CharField(max_length=255, choices=choices.RUNNING_STYLE.CHOICES(), verbose_name='前日脚質')
    dist_apt = models.PositiveSmallIntegerField(verbose_name='距離適性')
    prel_improvement = models.CharField(max_length=255, choices=choices.IMPROVEMENT.CHOICES(), verbose_name='前日上昇度コード')
    odds_win_base = models.FloatField(verbose_name='基準オッズ')
    pop_win_base = models.PositiveSmallIntegerField(verbose_name='基準人気順位')
    odds_show_base = models.FloatField(verbose_name='基準複勝オッズ')
    pop_show_base = models.PositiveSmallIntegerField(verbose_name='基準複勝人気順位')
    sym_sp_c_dbl = models.PositiveSmallIntegerField(verbose_name='特定情報◎')
    sym_sp_c = models.PositiveSmallIntegerField(verbose_name='特定情報○')
    sym_sp_t_dark = models.PositiveSmallIntegerField(verbose_name='特定情報▲')
    sym_sp_t = models.PositiveSmallIntegerField(verbose_name='特定情報△')
    sym_sp_x = models.PositiveSmallIntegerField(verbose_name='特定情報×')
    sym_total_c_dbl = models.PositiveSmallIntegerField(verbose_name='総合情報◎')
    sym_total_c = models.PositiveSmallIntegerField(verbose_name='総合情報○')
    sym_total_t_dark = models.PositiveSmallIntegerField(verbose_name='総合情報▲')
    sym_total_t = models.PositiveSmallIntegerField(verbose_name='総合情報△')
    sym_total_x = models.PositiveSmallIntegerField(verbose_name='総合情報×')
    trainer_outlook = models.CharField(max_length=255, choices=choices.TRAINER_HORSE_EVALUATION.CHOICES(),
                                       verbose_name='調教矢印コード')
    stable_outlook = models.CharField(max_length=255, choices=choices.STABLE_HORSE_EVALUATION.CHOICES(),
                                      verbose_name='厩舎評価コード')
    jockey_exp_1o2_place_rate = models.FloatField(verbose_name='騎手期待連対率',
                                                  help_text='騎手Ａが単勝基準オッズＢの馬に乗った場合の過去の成績を集計し、算出された連対率')
    paddock_observed_hoof = models.CharField(max_length=255, choices=choices.PADDOCK_OBSERVED_HOOF.CHOICES(),
                                             verbose_name='蹄コード')
    yield_track_apt = models.CharField(max_length=255, choices=choices.YIELDING_TRACK_APTITUDE.CHOICES(),
                                       verbose_name='重適正コード')
    blinker = models.CharField(max_length=255, choices=choices.BLINKER.CHOICES(), verbose_name='ブリンカー')
    post_position = models.PositiveSmallIntegerField(verbose_name='枠番')
    prel_b3f_time_idx = models.FloatField(null=True, verbose_name='予想テン指数')
    prel_pace_idx = models.FloatField(null=True, verbose_name='予想ペース指数')
    prel_f3f_time_idx = models.FloatField(null=True, verbose_name='予想上がり指数')
    prel_position_idx = models.FloatField(null=True, verbose_name='予想位置指数')
    prel_pace_cat = models.CharField(max_length=255, choices=choices.PACE_CATEGORY.CHOICES(), verbose_name='馬ペース')

    class Meta:
        db_table = 'contenders'
        unique_together = ('race', 'horse', 'jockey', 'trainer')
