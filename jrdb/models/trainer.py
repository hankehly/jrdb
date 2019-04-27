from django.contrib.postgres.fields import ArrayField
from django.db import models

from jrdb.models import choices


class Trainer(models.Model):
    code = models.CharField(max_length=5, unique=True)
    retired_on = models.DateField(null=True)
    name = models.CharField(max_length=12, null=True)
    name_kana = models.CharField(max_length=30, null=True)
    name_abbr = models.CharField(max_length=255, null=True)
    area = models.CharField(max_length=255, choices=choices.AREA.CHOICES(), null=True)
    training_center_name = models.CharField(max_length=4, null=True)
    birthday = models.DateField(null=True)
    lic_acquired_yr = models.PositiveIntegerField(null=True)
    jrdb_comment = models.CharField(max_length=40, null=True)
    jrdb_comment_date = models.DateField(null=True)
    cur_yr_leading = models.PositiveIntegerField(null=True)
    cur_yr_flat_r = ArrayField(models.PositiveSmallIntegerField(), size=4, null=True)
    cur_yr_obst_r = ArrayField(models.PositiveSmallIntegerField(), size=4, null=True)
    cur_yr_sp_wins = models.PositiveIntegerField(null=True)
    cur_yr_hs_wins = models.PositiveIntegerField(null=True)
    prev_yr_leading = models.PositiveIntegerField(null=True)
    prev_yr_flat_r = ArrayField(models.PositiveSmallIntegerField(), size=4, null=True)
    prev_yr_obst_r = ArrayField(models.PositiveSmallIntegerField(), size=4, null=True)
    prev_yr_sp_wins = models.PositiveIntegerField(null=True)
    prev_yr_hs_wins = models.PositiveIntegerField(null=True)
    sum_flat_r = ArrayField(models.PositiveSmallIntegerField(), size=4, null=True)
    sum_obst_r = ArrayField(models.PositiveSmallIntegerField(), size=4, null=True)
    jrdb_saved_on = models.DateField(null=True)

    class Meta:
        db_table = 'trainers'
