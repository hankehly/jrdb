from django.db import models

from jrdb.models import BaseModel


class Racetrack(BaseModel):
    # TODO: english racetrack name
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'racetracks'
