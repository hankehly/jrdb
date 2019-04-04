from django.db import models

from jrdb.models import BaseModel, choices


class Contender(BaseModel):
    race = models.ForeignKey('jrdb.Race', on_delete=models.CASCADE)
    horse = models.ForeignKey('jrdb.Horse', on_delete=models.CASCADE)
    jockey = models.ForeignKey('jrdb.Jockey', on_delete=models.CASCADE)
    trainer = models.ForeignKey('jrdb.Trainer', on_delete=models.CASCADE)
    num = models.PositiveSmallIntegerField()

    # SEDから取得（成績系）
    order_of_finish = models.PositiveSmallIntegerField()
    penalty = models.CharField(max_length=255, choices=choices.PENALTY.CHOICES())
    time = models.FloatField(null=True)
    mounted_weight = models.FloatField()
    odds_win = models.FloatField(null=True)
    popularity = models.PositiveSmallIntegerField()

    IDM = models.SmallIntegerField(null=True)
    speed_index = models.SmallIntegerField(null=True, help_text='素点')
    pace = models.SmallIntegerField(null=True)
    positioning = models.SmallIntegerField(null=True, help_text='位置取')
    late_start = models.PositiveSmallIntegerField(null=True, help_text='出遅')
    disadvt = models.PositiveSmallIntegerField(null=True, help_text='不利')
    b3f_disadvt = models.PositiveSmallIntegerField(null=True, help_text='前３Ｆ内での不利')
    mid_disadvt = models.PositiveSmallIntegerField(null=True, help_text='道中での不利')
    f3f_disadvt = models.PositiveSmallIntegerField(null=True, help_text='後３Ｆ内での不利')

    race_line = models.CharField(max_length=255, choices=choices.RACE_LINE.CHOICES(), help_text='コース取り')
    improvement = models.CharField(max_length=255, choices=choices.IMPROVEMENT.CHOICES(), help_text='上昇度コード')
    physique = models.CharField(max_length=255, choices=choices.PHYSIQUE.CHOICES(), help_text='馬体コード')
    demeanor = models.CharField(max_length=255, choices=choices.DEMEANOR.CHOICES(), help_text='気配コード')

    pace_cat = models.CharField(max_length=255, choices=choices.PACE_CATEGORY.CHOICES())
    b3f_time_index = models.FloatField(null=True)
    f3f_time_index = models.FloatField(null=True)
    pace_index = models.FloatField(null=True, help_text='馬のペースを指数化したもの')
    margin = models.FloatField(null=True, help_text='1(2)着タイム差')
    b3f_time = models.FloatField(null=True, help_text='前３Ｆタイム')
    f3f_time = models.FloatField(null=True, help_text='後３Ｆタイム')

    c1p = models.PositiveSmallIntegerField(null=True, help_text='コーナー順位1')
    c2p = models.PositiveSmallIntegerField(null=True, help_text='コーナー順位2')
    c3p = models.PositiveSmallIntegerField(null=True, help_text='コーナー順位3')
    c4p = models.PositiveSmallIntegerField(null=True, help_text='コーナー順位4')

    b3f_1p_margin = models.FloatField(null=True, help_text='前３Ｆ地点での先頭とのタイム差（0.1秒単位）')
    f3f_1p_margin = models.FloatField(null=True, help_text='後３Ｆ地点での先頭とのタイム差（0.1秒単位）')

    weight = models.PositiveSmallIntegerField(help_text='馬体重')
    weight_diff = models.SmallIntegerField(null=True, help_text='馬体重増減')

    running_style = models.CharField(max_length=255, choices=choices.RUNNING_STYLE.CHOICES())
    purse = models.FloatField()
    pace_flow = models.ForeignKey('jrdb.PaceFlowCode', null=True, on_delete=models.CASCADE)
    c4_race_line = models.CharField(max_length=255, choices=choices.RACE_LINE.CHOICES())

    # KYIから取得（前日系）
    jockey_index = models.FloatField(help_text='基準オッズと騎手の連対率の関係を基に算出された指数値')
    info_index = models.FloatField(help_text='基準オッズ、厩舎指数、調教指数等様々な情報を基に算出された指数値')
    total_index = models.FloatField(help_text='ＩＤＭ、騎手指数、情報指数を合計した値')
    rotation = models.PositiveSmallIntegerField(null=True, help_text='間に金曜日が入っている数で決定、連闘は０、初出走はnull')
    prior_IDM = models.SmallIntegerField(null=True)
    prior_running_style = models.CharField(max_length=255, choices=choices.RUNNING_STYLE.CHOICES())
    distance_aptitude = models.PositiveSmallIntegerField(help_text='距離適性')
    prior_improvement = models.CharField(max_length=255, choices=choices.IMPROVEMENT.CHOICES(), help_text='上昇度コード')
    odds_win_base = models.FloatField(help_text='基準オッズ')
    popularity_win_base = models.PositiveSmallIntegerField(help_text='基準人気順位')
    odds_show_base = models.FloatField(help_text='基準複勝オッズ')
    popularity_show_base = models.PositiveSmallIntegerField(help_text='基準複勝人気順位')
    journal_mark_special_c_dbl = models.PositiveSmallIntegerField(help_text='特定情報◎')
    journal_mark_special_c = models.PositiveSmallIntegerField(help_text='特定情報○')
    journal_mark_special_t_dark = models.PositiveSmallIntegerField(help_text='特定情報▲')
    journal_mark_special_t = models.PositiveSmallIntegerField(help_text='特定情報△')
    journal_mark_special_x = models.PositiveSmallIntegerField(help_text='特定情報×')
    journal_mark_total_c_dbl = models.PositiveSmallIntegerField(help_text='総合情報◎')
    journal_mark_total_c = models.PositiveSmallIntegerField(help_text='総合情報○')
    journal_mark_total_t_dark = models.PositiveSmallIntegerField(help_text='総合情報▲')
    journal_mark_total_t = models.PositiveSmallIntegerField(help_text='総合情報△')
    journal_mark_total_x = models.PositiveSmallIntegerField(help_text='総合情報×')
    popularity_index = models.PositiveSmallIntegerField(null=True, help_text='その馬の人気を指数化した値')
    trainer_index = models.FloatField(help_text='調教指数')
    stable_index = models.FloatField(help_text='厩舎指数')
    trainer_horse_evaluation = models.CharField(max_length=255, choices=choices.TRAINER_HORSE_EVALUATION.CHOICES(),
                                                help_text='調教矢印コード')
    stable_horse_evaluation = models.CharField(max_length=255, choices=choices.STABLE_HORSE_EVALUATION.CHOICES(),
                                               help_text='厩舎評価コード')
    jockey_expected_1or2_place_rate = models.FloatField(help_text='騎手期待連対率')
    flat_out_run_index = models.SmallIntegerField()
    paddock_observed_hoof = models.CharField(max_length=255, choices=choices.PADDOCK_OBSERVED_HOOF.CHOICES(),
                                             help_text='蹄コード')
    yielding_track_aptitude = models.CharField(max_length=255, choices=choices.YIELDING_TRACK_APTITUDE.CHOICES(),
                                               help_text='重適正コード')
    blinker_usage = models.CharField(max_length=255, choices=choices.BLINKER_USAGE.CHOICES(), help_text='ブリンカー')

    class Meta:
        db_table = 'contenders'
        unique_together = ('race', 'horse', 'jockey', 'trainer')
