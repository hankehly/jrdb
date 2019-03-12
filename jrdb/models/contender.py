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

    # 1:A,2:A1,3:A2,4:B,5:C,6:D
    # This should be on the Race model (unless you can show that horses in same race can have different values)
    A = 'A'
    A1 = 'A1'
    A2 = 'A2'
    B = 'B'
    C = 'C'
    D = 'D'
    COURSE_LABEL_CHOICES = (
        (A, 'A'),
        (A1, 'A1'),
        (A2, 'A2'),
        (B, 'B'),
        (C, 'C'),
        (D, 'D'),
    )


