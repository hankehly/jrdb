from django.db import models

from jrdb.models.base import BaseModel
from jrdb.models.choices import HAIR_COLOR, HORSE_SYMBOL, SEX


class Horse(BaseModel):
    pedigree_reg_num = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=36)
    sex = models.CharField(max_length=255, choices=SEX.CHOICES)
    hair_color = models.CharField(max_length=255, choices=HAIR_COLOR.CHOICES)
    symbol = models.CharField(max_length=255, choices=HORSE_SYMBOL.CHOICES, null=True)
    sire_name = models.CharField(max_length=36)
    dam_name = models.CharField(max_length=36)
    damsire_name = models.CharField(max_length=36)
    birthday = models.DateField()
    sire_birth_yr = models.PositiveIntegerField()
    dam_birth_yr = models.PositiveIntegerField()
    damsire_birth_yr = models.PositiveIntegerField(null=True)
    owner_name = models.CharField(max_length=40)
    owner_racetrack = models.ForeignKey('jrdb.Racetrack', null=True, on_delete=models.SET_NULL)
    breeder_name = models.CharField(max_length=40)
    breeding_loc_name = models.CharField(max_length=8)
    is_retired = models.BooleanField()
    sire_genealogy_code = models.CharField(max_length=4)
    damsire_genealogy_code = models.CharField(max_length=4)

    class Meta:
        db_table = 'horses'
