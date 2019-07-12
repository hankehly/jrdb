import datetime
import os

from django.forms import model_to_dict

from jrdb.models import choices, Jockey
from jrdb.tests.base import JRDBTestCase, SAMPLES_DIR
from jrdb.templates import KZA


class KZATestCase(JRDBTestCase):
    fixtures = ["racetrack"]

    @classmethod
    def setUpTestData(cls):
        template_path = os.path.join(SAMPLES_DIR, "KSA020907.txt")
        t = KZA(template_path).extract()

        # only import the first row to make
        # test record easy to identify
        t.df = t.df.iloc[0].to_frame().T
        t.load()

        cls.jockey = Jockey.objects.first()

    def test_load_jockey(self):
        act = model_to_dict(self.jockey)
        exp = {
            "code": "10076",
            "retired_on": None,
            "name": "岡部幸雄",
            "name_kana": "オカベ ユキオ",
            "name_abbr": "岡 部",
            "area": choices.AREA.KANTOU,
            "training_center_name": None,
            "birthday": datetime.date(1948, 10, 31),
            "lic_acquired_yr": 1967,
            "jrdb_comment": "まだまだ衰え見られず。長距離戦は一級品。",
            "jrdb_comment_date": datetime.date(2002, 8, 15),
            "cur_yr_leading": 6,
            "cur_yr_flat_r": [52, 52, 40, 254],
            "cur_yr_obst_r": [0, 0, 0, 0],
            "cur_yr_sp_wins": 19,
            "cur_yr_hs_wins": 4,
            "prev_yr_leading": 3,
            "prev_yr_flat_r": [101, 67, 53, 418],
            "prev_yr_obst_r": [0, 0, 0, 0],
            "prev_yr_sp_wins": 38,
            "prev_yr_hs_wins": 4,
            "sum_flat_r": [2832, 2339, 2106, 10448],
            "sum_obst_r": [15, 9, 5, 33],
            "jrdb_saved_on": datetime.date(2002, 9, 7),
        }
        self.assertSubDict(exp, act)
