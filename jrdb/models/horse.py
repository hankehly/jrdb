from django.db import models

from jrdb.models.base import BaseModel


class Horse(BaseModel):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    CASTRATED = 'CASTRATED'
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (CASTRATED, 'Castrated')
    )

    pedigree_reg_num = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=36)
    sex = models.CharField(max_length=255, choices=SEX_CHOICES)
    hair_color_code = models.ForeignKey('jrdb.HairColorCode', on_delete=models.CASCADE)
    symbol = models.ForeignKey('jrdb.HorseSymbol', null=True, on_delete=models.SET_NULL)
    sire_name = models.CharField(max_length=36)
    dam_name = models.CharField(max_length=36)
    damsire_name = models.CharField(max_length=36)
    birthday = models.DateField()
    sire_birth_yr = models.PositiveIntegerField()
    dam_birth_yr = models.PositiveIntegerField()
    damsire_birth_yr = models.PositiveIntegerField(null=True)
    owner_name = models.CharField(max_length=40)
    owner_racetrack_code = models.ForeignKey('jrdb.RacetrackCode', null=True, on_delete=models.SET_NULL)
    breeder_name = models.CharField(max_length=40)
    breeding_loc_name = models.CharField(max_length=8)
    is_retired = models.BooleanField()
    sire_genealogy_code = models.CharField(max_length=4)
    damsire_genealogy_code = models.CharField(max_length=4)

    class Meta:
        db_table = 'horses'
