import os

from django.forms import model_to_dict

from jrdb.models import Contender, Horse, Program, Race
from jrdb.tests.base import JRDBTestCase, SAMPLES_DIR
from jrdb.templates import SKB


class SKBTestCase(JRDBTestCase):
    fixtures = ["racetrack", "horse_gear_code"]

    @classmethod
    def setUpTestData(cls):
        template_path = os.path.join(SAMPLES_DIR, "SKB020908.txt")
        t = SKB(template_path).extract()

        t.df = t.df.iloc[126].to_frame().T.reset_index(drop=True)  # line 252
        t.load()

        cls.program = Program.objects.first()
        cls.race = Race.objects.first()
        cls.horse = Horse.objects.first()
        cls.contender = Contender.objects.first()

    def test_load_program(self):
        act = model_to_dict(self.program)
        exp = {"racetrack": 1, "yr": 2, "round": 2, "day": "2"}
        self.assertSubDict(exp, act)

    def test_load_race(self):
        act = model_to_dict(self.race)
        exp = {"num": 10}
        self.assertSubDict(exp, act)

    def test_load_horse(self):
        act = model_to_dict(self.horse)
        exp = {"pedigree_reg_num": "99101111"}
        self.assertSubDict(exp, act)

    def test_load_contender(self):
        act = model_to_dict(self.contender)
        exp = {
            "num": 6,
            "sp_mention": ["415", "177", "722", None, None, None],
            "horse_gear": ["008", "009", "021", "040", "068", None, None, None],
            "hoof_overall": ["113", None, None],
            "hoof_front_left": [None, None, None],
            "hoof_front_right": [None, None, None],
            "hoof_back_left": ["000", None, None],
            "hoof_back_right": ["000", None, None],
            "paddock_comment": "トモ確り。フックラし、随分良くなった印象",
            "hoof_comment": "両後バンテージ。",
            "horse_gear_or_other_comment": "出負け。大外から良い伸び。",
            "race_comment": "出負け、後方から。大外から凄い脚で連絡む",
            "bit": 35,
            "bandage": True,
            "horseshoe": None,
            "hoof_cond": None,
            "periostitis": None,
            "exostosis": None,
        }
        self.assertSubDict(exp, act)
