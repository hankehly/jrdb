import datetime
import os

from django.forms import model_to_dict

from jrdb.models import choices, Horse
from jrdb.tests.base import JRDBTestCase, SAMPLES_DIR
from jrdb.templates import UKC


class UKCTestCase(JRDBTestCase):
    fixtures = ["racetrack", "pedigree"]

    @classmethod
    def setUpTestData(cls):
        template_path = os.path.join(SAMPLES_DIR, "UKC020908.txt")
        t = UKC(template_path).extract()

        # only import the first row to make
        # test record easy to identify
        t.df = t.df.iloc[0].to_frame().T
        t.load()

        cls.horse = Horse.objects.first()

    def test_load_horse(self):
        act = model_to_dict(self.horse)
        exp = {
            "pedigree_reg_num": "99101712",
            "name": "アドマイヤエディ",
            "sex": choices.SEX.MALE,
            "hair_color": choices.HAIR_COLOR.BAY,
            "symbol": choices.HORSE_SYMBOL.NA,
            "sire_name": "コマンダーインチーフ",
            "dam_name": "アドマイヤエール",
            "damsire_name": "ジェネラス",
            "birthday": datetime.date(1999, 5, 31),
            "sire_birth_yr": 1990,
            "dam_birth_yr": 1993,
            "damsire_birth_yr": 1988,
            "owner_name": "近藤 利一氏",
            "owner_racetrack": 9,
            "breeder_name": "辻 牧場",
            "breeding_loc_name": "浦河",
            "is_retired": False,
            "jrdb_saved_on": datetime.date(2002, 9, 8),
            "pedigree_sire": 4,
            "pedigree_damsire": 2,
        }
        self.assertSubDict(exp, act)
