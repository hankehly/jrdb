from django.db import models


class Racetrack(models.Model):
    # TODO: english racetrack name
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'racetracks'
