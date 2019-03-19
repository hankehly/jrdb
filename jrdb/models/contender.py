from django.db import models

from jrdb.models import BaseModel
from jrdb.models.choices import PACE_CATEGORY, RACE_LINE, PENALTY, IMPROVEMENT, PHYSIQUE, DEMEANOR, RUNNING_STYLE


class Contender(BaseModel):
    """
    IDM = speed_index + pace + ハンデ(斤量補正) + memory factors

    pace - ペース
    テン（前半３ハロン）・上がり（後半３ハロン）と、それを除いた道中のペースを加味

    TODO: positioning 位置取 の意味/単位を明記 (1, 2, 3, na, ..)

    memory factors (mf) 記憶要素
    馬身単位 (1 = 1馬身 ... IDMに1点を加点)

    late_start - 出遅
    例）ゲートを出ない・出が悪い

    disadvantage - 不利
    例）直線で前が詰まり他馬に1馬身遅れたなど
    """
    race = models.ForeignKey('jrdb.Race', on_delete=models.CASCADE)
    horse = models.ForeignKey('jrdb.Horse', on_delete=models.CASCADE)
    jockey = models.ForeignKey('jrdb.Jockey', on_delete=models.CASCADE)
    trainer = models.ForeignKey('jrdb.Trainer', on_delete=models.CASCADE)
    num = models.PositiveSmallIntegerField()
    order_of_finish = models.PositiveSmallIntegerField()
    penalty = models.CharField(max_length=255, choices=PENALTY.CHOICES())
    time = models.FloatField()
    mounted_weight = models.FloatField()
    odds_win = models.FloatField()
    popularity = models.PositiveSmallIntegerField()

    IDM = models.SmallIntegerField()
    speed_index = models.SmallIntegerField(help_text='素点')
    pace = models.PositiveSmallIntegerField(null=True)
    positioning = models.PositiveSmallIntegerField(null=True, help_text='位置取')
    late_start = models.PositiveSmallIntegerField(null=True, help_text='出遅')
    disadvt = models.PositiveSmallIntegerField(null=True, help_text='不利')
    b3f_disadvt = models.PositiveSmallIntegerField(null=True, help_text='前３Ｆ内での不利')
    mid_disadvt = models.PositiveSmallIntegerField(null=True, help_text='道中での不利')
    f3f_disadvt = models.PositiveSmallIntegerField(null=True, help_text='後３Ｆ内での不利')

    race_line = models.CharField(max_length=255, choices=RACE_LINE.CHOICES(), help_text='コース取り')
    improvement = models.CharField(max_length=255, choices=IMPROVEMENT.CHOICES(), help_text='上昇度コード')
    physique = models.CharField(max_length=255, choices=PHYSIQUE.CHOICES(), help_text='馬体コード')
    demeanor = models.CharField(max_length=255, choices=DEMEANOR.CHOICES(), help_text='気配コード')

    pace_cat = models.CharField(max_length=255, choices=PACE_CATEGORY.CHOICES())
    b3f_time_index = models.FloatField(null=True)
    f3f_time_index = models.FloatField(null=True)
    pace_index = models.FloatField(null=True, help_text='馬のペースを指数化したもの')
    margin = models.FloatField(help_text='1(2)着タイム差')
    b3f_time = models.FloatField(help_text='前３Ｆタイム')
    f3f_time = models.FloatField(help_text='後３Ｆタイム')

    c1p = models.PositiveSmallIntegerField(null=True, help_text='コーナー順位1')
    c2p = models.PositiveSmallIntegerField(null=True, help_text='コーナー順位2')
    c3p = models.PositiveSmallIntegerField(null=True, help_text='コーナー順位3')
    c4p = models.PositiveSmallIntegerField(null=True, help_text='コーナー順位4')

    b3f_1p_margin = models.FloatField(null=True, help_text='前３Ｆ地点での先頭とのタイム差（0.1秒単位）')
    f3f_1p_margin = models.FloatField(null=True, help_text='後３Ｆ地点での先頭とのタイム差（0.1秒単位）')

    weight = models.PositiveSmallIntegerField(help_text='馬体重')
    weight_diff = models.PositiveSmallIntegerField(null=True, help_text='馬体重増減')

    running_style = models.CharField(max_length=255, choices=RUNNING_STYLE.CHOICES())
    purse = models.PositiveSmallIntegerField()
    pace_flow = models.ForeignKey('jrdb.PaceFlowCode', null=True, on_delete=models.CASCADE)
    c4_race_line = models.CharField(max_length=255, choices=RACE_LINE.CHOICES())

    class Meta:
        db_table = 'contenders'
