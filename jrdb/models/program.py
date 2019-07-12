from django.db import models

from jrdb.models import choices
from jrdb.models.managers import DataFrameQuerySet


class Program(models.Model):
    racetrack = models.ForeignKey("jrdb.Racetrack", on_delete=models.CASCADE)
    yr = models.PositiveSmallIntegerField()
    round = models.PositiveSmallIntegerField()
    day = models.CharField(max_length=1)

    # KAB
    weather = models.CharField(
        "天候", max_length=255, choices=choices.WEATHER.CHOICES(), null=True
    )
    host_category = models.CharField(
        max_length=255, choices=choices.HOST_CATEGORY.CHOICES(), null=True
    )
    nth_occurrence = models.PositiveSmallIntegerField(null=True)
    turf_cond = models.CharField(
        "芝馬場状態", max_length=255, null=True, choices=choices.TRACK_CONDITION_KA.CHOICES()
    )
    turf_cond_inner = models.CharField(
        "芝馬場状態内",
        max_length=255,
        null=True,
        choices=choices.TRACK_CONDITION_KA.CHOICES(),
    )
    turf_cond_mid = models.CharField(
        "芝馬場状態中",
        max_length=255,
        null=True,
        choices=choices.TRACK_CONDITION_KA.CHOICES(),
    )
    turf_cond_outer = models.CharField(
        "芝馬場状態外",
        max_length=255,
        null=True,
        choices=choices.TRACK_CONDITION_KA.CHOICES(),
    )
    turf_speed_shift = models.SmallIntegerField("芝馬場差", null=True)
    hs_speed_shift_innermost = models.SmallIntegerField("直線馬場差最内", null=True)
    hs_speed_shift_inner = models.SmallIntegerField("直線馬場差内", null=True)
    hs_speed_shift_mid = models.SmallIntegerField("直線馬場差中", null=True)
    hs_speed_shift_outer = models.SmallIntegerField("直線馬場差外", null=True)
    hs_speed_shift_outermost = models.SmallIntegerField("直線馬場差大外", null=True)
    dirt_cond = models.CharField(
        "ダ馬場状態", max_length=255, null=True, choices=choices.TRACK_CONDITION_KA.CHOICES()
    )
    dirt_cond_inner = models.CharField(
        "ダ馬場状態内",
        max_length=255,
        null=True,
        choices=choices.TRACK_CONDITION_KA.CHOICES(),
    )
    dirt_cond_mid = models.CharField(
        "ダ馬場状態中",
        max_length=255,
        null=True,
        choices=choices.TRACK_CONDITION_KA.CHOICES(),
    )
    dirt_cond_outer = models.CharField(
        "ダ馬場状態外",
        max_length=255,
        null=True,
        choices=choices.TRACK_CONDITION_KA.CHOICES(),
    )
    dirt_speed_shift = models.SmallIntegerField("ダ馬場差", null=True)
    turf_type = models.CharField(
        "芝種類", max_length=255, null=True, choices=choices.TURF_TYPE.CHOICES()
    )
    grass_height = models.FloatField("草丈", null=True)
    used_rolling_compactor = models.BooleanField("転圧", null=True)
    used_anti_freeze_agent = models.BooleanField("凍結防止剤", null=True)
    mm_precipitation = models.FloatField("中間降水量", null=True)

    objects = DataFrameQuerySet.as_manager()

    class Meta:
        db_table = "programs"
        unique_together = ("racetrack", "yr", "round", "day")
