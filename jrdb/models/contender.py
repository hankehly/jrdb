from jrdb.models import BaseModel


class Contender(BaseModel):
    # レースのペース（先頭馬のペース）をコース、距離、クラス別で計算。
    # This should be on the Race model (unless you can show that horses in same race can have different values)
    HIGH = 'HIGH',
    NORMAL = 'NORMAL'
    SLOW = 'SLOW'
    PACE_CHOICES = (
        (HIGH, 'ハイ'),
        (NORMAL, '平均'),
        (SLOW, 'スロー'),
    )
