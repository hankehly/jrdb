from django.db import models

from jrdb.models import choices
from jrdb.models.managers import DataFrameQuerySet


class Horse(models.Model):
    pedigree_reg_num = models.CharField(max_length=8)
    name = models.CharField(max_length=36, null=True)
    sex = models.CharField(verbose_name='性別', max_length=255, null=True, choices=choices.SEX.CHOICES())
    hair_color = models.CharField(max_length=255, null=True, choices=choices.HAIR_COLOR.CHOICES())
    symbol = models.CharField(verbose_name='馬記号', max_length=255, null=True, choices=choices.HORSE_SYMBOL.CHOICES())
    sire_name = models.CharField(max_length=36, null=True)
    dam_name = models.CharField(max_length=36, null=True)
    damsire_name = models.CharField(max_length=36, null=True)
    birthday = models.DateField(null=True)
    sire_birth_yr = models.PositiveSmallIntegerField(null=True)
    dam_birth_yr = models.PositiveSmallIntegerField(null=True)
    damsire_birth_yr = models.PositiveSmallIntegerField(null=True)
    owner_name = models.CharField(verbose_name='馬主名', max_length=255, null=True)
    owner_racetrack = models.ForeignKey('jrdb.Racetrack', models.SET_NULL, verbose_name='馬主会', null=True)
    breeder_name = models.CharField(max_length=255, null=True)
    breeding_loc_name = models.CharField(max_length=8, null=True)
    is_retired = models.NullBooleanField()
    pedigree_sire = models.ForeignKey('jrdb.Pedigree', models.SET_NULL, null=True, related_name='pedigree_sire')
    pedigree_damsire = models.ForeignKey('jrdb.Pedigree', models.SET_NULL, null=True, related_name='pedigree_damsire')
    jrdb_saved_on = models.DateField(null=True)

    objects = DataFrameQuerySet.as_manager()

    class Meta:
        db_table = 'horses'
        unique_together = ('pedigree_reg_num',)
