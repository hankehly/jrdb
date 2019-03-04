from django.db import models

from jrdb.models.base import BaseModel


class Horse(BaseModel):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    CASTRATED = 'CASTRATED'
    SEX = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (CASTRATED, 'Castrated')
    )

    CHESTNUT = 'CHESTNUT'
    DARK_CHESTNUT = 'DARK_CHESTNUT'
    BAY = 'BAY'
    DARK_BAY = 'DARK_BAY'
    BROWN = 'BROWN'
    BLACK = 'BLACK'
    GRAY = 'GRAY'
    RED_ROAN = 'RED_ROAN'
    BAY_ROAN = 'BAY_ROAN'
    BLUE_ROAN = 'BLUE_ROAN'
    WHITE = 'WHITE'
    HAIR_COLOR = (
        (CHESTNUT, 'Chestnut'),
        (DARK_CHESTNUT, 'Dark chestnut'),
        (BAY, 'Bay'),
        (DARK_BAY, 'Dark bay'),
        (BROWN, 'Brown'),
        (BLACK, 'Black'),
        (GRAY, 'Gray'),
        (RED_ROAN, 'Red roan'),
        (BAY_ROAN, 'Bay roan'),
        (BLUE_ROAN, 'Blue roan'),
        (WHITE, 'WHITE'),
    )

    prn = models.CharField(max_length=8, unique=True, verbose_name='Pedigree Registration Number')
    name = models.CharField(max_length=36)

    # TODO: Move to separate table
    # Valid values are _data_ not code. They belong in the database.
    # Use fixtures files to organize
    # https://softwareengineering.stackexchange.com/questions/305148/why-would-you-store-an-enum-in-db
    # sex = models.CharField(max_length=255, choices=SEX)
    # hair_color = models.CharField(max_length=255, choices=HAIR_COLOR)

    class Meta:
        db_table = 'horses'
