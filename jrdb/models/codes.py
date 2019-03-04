from django.db import models

from jrdb.models import BaseModel


class RunningStyle(BaseModel):
    """
    脚質コード（競走馬が得意とする走り）
    過去の競走実績よりその馬の脚質を判断したコード。
    """
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)


class SpecialMention(BaseModel):
    """
    特記コード

    http://www.jrdb.com/program/tokki_code.txt
    """
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
