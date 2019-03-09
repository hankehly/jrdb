from django.core.validators import validate_comma_separated_integer_list
from django.db import models

from jrdb.models.base import BaseModel


class Trainer(BaseModel):
    KANTOU = 'KANTOU'
    KANSAI = 'KANSAI'
    OTHER = 'OTHER'
    AREA_CHOICES = (
        (KANSAI, '関東'),
        (KANTOU, '関西'),
        (OTHER, '他'),
    )

    code = models.CharField(max_length=5, unique=True)
    retired_on = models.DateField(null=True)
    name = models.CharField(max_length=12)
    name_kana = models.CharField(max_length=30)
    name_abbr = models.CharField(max_length=6)
    area = models.CharField(max_length=255, choices=AREA_CHOICES)
    training_center_name = models.CharField(max_length=4)
    birthday = models.DateField()
    lic_acquired_yr = models.PositiveIntegerField()
    jrdb_comment = models.CharField(max_length=40)
    jrdb_comment_date = models.DateField(null=True)
    cur_yr_leading = models.PositiveIntegerField(null=True)
    cur_yr_flat_r = models.CharField(max_length=12, validators=[validate_comma_separated_integer_list])
    cur_yr_obst_r = models.CharField(max_length=12, validators=[validate_comma_separated_integer_list])
    cur_yr_sp_wins = models.PositiveIntegerField()
    cur_yr_hs_wins = models.PositiveIntegerField()
    prev_yr_leading = models.PositiveIntegerField(null=True)
    prev_yr_flat_r = models.CharField(max_length=12, validators=[validate_comma_separated_integer_list])
    prev_yr_obst_r = models.CharField(max_length=12, validators=[validate_comma_separated_integer_list])
    prev_yr_sp_wins = models.PositiveIntegerField()
    prev_yr_hs_wins = models.PositiveIntegerField()
    sum_flat_r = models.CharField(max_length=20, validators=[validate_comma_separated_integer_list])
    sum_obst_r = models.CharField(max_length=20, validators=[validate_comma_separated_integer_list])

    class Meta:
        db_table = 'trainers'
