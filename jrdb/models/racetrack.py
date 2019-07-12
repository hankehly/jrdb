from django.db import models


class Racetrack(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)

    class Meta:
        db_table = "racetracks"
