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

    # codes
    racetrack = models.ForeignKey('jrdb.RacetrackCode', on_delete=models.CASCADE)
    category = models.ForeignKey('jrdb.RaceCategoryCode', on_delete=models.CASCADE)
    cond = models.ForeignKey('jrdb.RaceConditionCode', on_delete=models.CASCADE)
    horse_sex_symbol = models.ForeignKey('jrdb.RaceHorseSexSymbol', on_delete=models.CASCADE)
    horse_type_symbol = models.ForeignKey('jrdb.RaceHorseTypeSymbol', on_delete=models.CASCADE)
    interleague_symbol = models.ForeignKey('jrdb.RaceInterleagueSymbol', on_delete=models.CASCADE)
    impost_class = models.ForeignKey('jrdb.ImpostClassCode', on_delete=models.CASCADE)
    grade = models.ForeignKey('jrdb.GradeCode', on_delete=models.CASCADE)
    track_cond = models.ForeignKey('jrdb.TrackConditionCode', on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    name_abbr = models.CharField(max_length=8)
    name_short = models.CharField(max_length=18)

    # composed of year/month/date + hh/mm from separate files
    started_at = models.DateTimeField()

    # program related data
    round = models.PositiveSmallIntegerField()
    day = models.PositiveIntegerField()
    num = models.PositiveSmallIntegerField()

    distance = models.PositiveIntegerField()
    surface = models.CharField(max_length=255, choices=SURFACE_CHOICES)
    direction = models.CharField(max_length=255, choices=DIRECTION_CHOICES)
    course_inout = models.CharField(max_length=255, choices=COURSE_INOUT_CHOICES)
    course_label = models.CharField(max_length=255, choices=COURSE_LABEL_CHOICES)
