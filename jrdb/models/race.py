from django.core.validators import validate_comma_separated_integer_list
from django.db import models

from jrdb.models import BaseModel


class Race(BaseModel):
    OTHER = 'OTHER'

    TURF = 'TURF'
    DIRT = 'DIRT'
    OBSTACLE = 'OBSTACLE'
    SURFACE_CHOICES = (
        (TURF, '芝'),
        (DIRT, 'ダート'),
        (OBSTACLE, '障害'),
    )

    RIGHT = 'RIGHT'
    LEFT = 'LEFT'
    STRAIGHT = 'STRAIGHT'
    DIRECTION_CHOICES = (
        (RIGHT, '右'),
        (LEFT, '左'),
        (STRAIGHT, '直'),
        (OTHER, '他'),
    )

    INSIDE = 'INSIDE'
    OUTSIDE = 'OUTSIDE'
    STRAIGHT_DIRT = 'STRAIGHT_DIRT'
    COURSE_INOUT_CHOICES = (
        (INSIDE, '通常(内)'),
        (OUTSIDE, '外'),
        (STRAIGHT_DIRT, '直ダ'),
        (OTHER, '他'),
    )

    A = 'A'
    A1 = 'A1'
    A2 = 'A2'
    B = 'B'
    C = 'C'
    D = 'D'
    COURSE_LABEL_CHOICES = (
        (A, 'A'),
        (A1, 'A1'),
        (A2, 'A2'),
        (B, 'B'),
        (C, 'C'),
        (D, 'D'),
    )

    # key related data
    racetrack = models.ForeignKey('jrdb.RacetrackCode', on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    round = models.PositiveSmallIntegerField()
    day = models.PositiveSmallIntegerField()
    num = models.PositiveSmallIntegerField()

    # codes
    category = models.ForeignKey('jrdb.RaceCategoryCode', on_delete=models.SET_NULL, null=True)
    cond = models.ForeignKey('jrdb.RaceConditionCode', on_delete=models.SET_NULL, null=True)
    horse_sex_symbol = models.ForeignKey('jrdb.RaceHorseSexSymbol', on_delete=models.SET_NULL, null=True)
    horse_type_symbol = models.ForeignKey('jrdb.RaceHorseTypeSymbol', on_delete=models.SET_NULL, null=True)
    interleague_symbol = models.ForeignKey('jrdb.RaceInterleagueSymbol', on_delete=models.SET_NULL, null=True)
    impost_class = models.ForeignKey('jrdb.ImpostClassCode', on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey('jrdb.GradeCode', on_delete=models.SET_NULL, null=True)
    track_cond = models.ForeignKey('jrdb.TrackConditionCode', on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=50, null=True)
    name_abbr = models.CharField(max_length=8, null=True)
    name_short = models.CharField(max_length=18, null=True)

    # composed of year/month/date + hh/mm from separate files
    started_at = models.DateTimeField(null=True)

    distance = models.PositiveSmallIntegerField(null=True)
    surface = models.CharField(max_length=255, choices=SURFACE_CHOICES, null=True)
    direction = models.CharField(max_length=255, choices=DIRECTION_CHOICES, null=True)
    course_inout = models.CharField(max_length=255, choices=COURSE_INOUT_CHOICES, null=True)
    course_label = models.CharField(max_length=255, choices=COURSE_LABEL_CHOICES, null=True)
    comment = models.TextField(max_length=500)

    # track bias
    track_bias_1C = models.CharField(
        max_length=255,
        validators=[validate_comma_separated_integer_list],
        verbose_name='Corner 1 track bias',
        help_text='（内、中、外）',
        null=True
    )

    track_bias_2C = models.CharField(
        max_length=255,
        validators=[validate_comma_separated_integer_list],
        verbose_name='Corner 2 track bias',
        help_text='（内、中、外）',
        null=True
    )

    track_bias_3C = models.CharField(
        max_length=255,
        validators=[validate_comma_separated_integer_list],
        verbose_name='Corner 3 track bias',
        help_text='（内、中、外）',
        null=True
    )

    track_bias_4C = models.CharField(
        max_length=255,
        validators=[validate_comma_separated_integer_list],
        verbose_name='Corner 4 track bias',
        help_text='（最内、内、中、外、大外）',
        null=True
    )

    track_bias_bs = models.CharField(
        max_length=255,
        validators=[validate_comma_separated_integer_list],
        verbose_name='Backstretch track bias',
        help_text='（内、中、外）',
        null=True
    )

    track_bias_hs = models.CharField(
        max_length=255,
        validators=[validate_comma_separated_integer_list],
        verbose_name='Homestretch track bias',
        help_text='（最内、内、中、外、大外）',
        null=True
    )

    class Meta:
        unique_together = ('racetrack', 'year', 'round', 'day', 'num')
