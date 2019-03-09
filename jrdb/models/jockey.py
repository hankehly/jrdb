from django.core.validators import validate_comma_separated_integer_list
from django.db import models

from jrdb.models import BaseModel


class Jockey(BaseModel):
    KANTOU = 'KANTOU'
    KANSAI = 'KANSAI'
    OTHER = 'OTHER'
    AREA_CHOICES = (
        (KANSAI, '関東'),
        (KANTOU, '関西'),
        (OTHER, '他'),
    )

    # 1: (1K減) ☆
    # 2: (2K減) △
    # 3: (3K減) ▲
    # http://www.jra.go.jp/kouza/yougo/w574.html
    REDUCE_1K = 'REDUCE_1'
    REDUCE_2K = 'REDUCE_2'
    REDUCE_3K = 'REDUCE_3'
    TRAINEE_CATEGORY_CHOICES = (
        (REDUCE_1K, '1K減'),
        (REDUCE_2K, '2K減'),
        (REDUCE_3K, '3K減'),
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
    trainee_cat = models.CharField(max_length=255, choices=TRAINEE_CATEGORY_CHOICES)
    # TODO: 所属厩舎 (trainer_code) can this be a key?
    trainer_code = models.CharField(max_length=5, unique=True)
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
        db_table = 'jockeys'
