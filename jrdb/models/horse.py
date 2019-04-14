from django.db import models

from . import BaseModel, choices


class Horse(BaseModel):
    pedigree_reg_num = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=36)
    sex = models.CharField(max_length=255, choices=choices.SEX.CHOICES(), null=True)
    hair_color = models.CharField(max_length=255, choices=choices.HAIR_COLOR.CHOICES(), null=True)
    symbol = models.CharField(max_length=255, choices=choices.HORSE_SYMBOL.CHOICES(), null=True)
    sire_name = models.CharField(max_length=36, null=True)
    dam_name = models.CharField(max_length=36, null=True)
    damsire_name = models.CharField(max_length=36, null=True)
    birthday = models.DateField(null=True)
    sire_birth_yr = models.PositiveSmallIntegerField(null=True)
    dam_birth_yr = models.PositiveSmallIntegerField(null=True)
    damsire_birth_yr = models.PositiveSmallIntegerField(null=True)
    owner_name = models.CharField(max_length=40, null=True)
    owner_racetrack = models.ForeignKey('jrdb.Racetrack', null=True, on_delete=models.SET_NULL)
    breeder_name = models.CharField(max_length=40, null=True)
    breeding_loc_name = models.CharField(max_length=8, null=True)
    is_retired = models.NullBooleanField()
    sire_genealogy_code = models.CharField(max_length=4, null=True)
    damsire_genealogy_code = models.CharField(max_length=4, null=True)
    jrdb_saved_on = models.DateField(null=True)

    class Meta:
        db_table = 'horses'
