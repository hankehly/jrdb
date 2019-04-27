from django.db import models

from . import choices


class Horse(models.Model):
    pedigree_reg_num = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=36)
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
    owner_name = models.CharField(verbose_name='馬主名', max_length=40, null=True)
    owner_racetrack = models.ForeignKey('jrdb.Racetrack', on_delete=models.SET_NULL, verbose_name='馬主会', null=True)
    breeder_name = models.CharField(max_length=40, null=True)
    breeding_loc_name = models.CharField(max_length=8, null=True)
    is_retired = models.NullBooleanField()
    sire_genealogy_code = models.CharField(max_length=4, null=True)
    damsire_genealogy_code = models.CharField(max_length=4, null=True)
    jrdb_saved_on = models.DateField(null=True)

    class Meta:
        db_table = 'horses'
