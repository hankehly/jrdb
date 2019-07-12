import os

from django.forms import model_to_dict

from jrdb.models import choices, Program, Race, Contender, Horse, Trainer, Jockey
from jrdb.tests.base import JRDBTestCase, SAMPLES_DIR
from jrdb.templates import SED


class SEDTestCase(JRDBTestCase):
    fixtures = ["pace_flow_code", "race_condition_code", "racetrack"]

    @classmethod
    def setUpTestData(cls):
        template_path = os.path.join(SAMPLES_DIR, "SED080913.txt")
        t = SED(template_path).extract()

        t.df = t.df.iloc[318].to_frame().T.reset_index(drop=True)
        t.load()

        cls.program = Program.objects.first()
        cls.race = Race.objects.first()
        cls.horse = Horse.objects.first()
        cls.trainer = Trainer.objects.first()
        cls.jockey = Jockey.objects.first()
        cls.contender = Contender.objects.first()

    def test_load_program(self):
        act = model_to_dict(self.program)
        exp = {"racetrack": 6, "yr": 8, "round": 4, "day": "1"}
        self.assertSubDict(exp, act)

    def test_load_race(self):
        act = model_to_dict(self.race)
        exp = {
            "num": 12,
            "distance": 1600,
            "surface": choices.SURFACE.TURF,
            "direction": choices.DIRECTION.RIGHT,
            "course_inout": choices.COURSE_INOUT.OUTSIDE,
            "track_cond": choices.TRACK_CONDITION.FIRM_FAST,
            "category": choices.RACE_CATEGORY.THREE_YR_OLD_AND_UP,
            "cond": 2,
            "horse_type_symbol": choices.RACE_HORSE_TYPE_SYMBOL.MIX,
            "horse_sex_symbol": choices.RACE_HORSE_SEX_SYMBOL.NA,
            "interleague_symbol": choices.RACE_INTERLEAGUE_SYMBOL.DES,
            "impost_class": choices.IMPOST_CLASS.SPECIAL_WEIGHT_AGE_SEX,
            "grade": None,
            "name": None,
            "contender_count": 16,
            "name_abbr": None,
            "track_speed_shift": -14,
            "pace_cat": choices.PACE_CATEGORY.HIGH,
            "pace_idx": 14.5,
            "weather": choices.WEATHER.FINE,
            "course_label": choices.COURSE_LABEL.B,
            "pace_flow": 6,
        }
        self.assertSubDict(exp, act)

    def test_load_horse(self):
        act = model_to_dict(self.horse)
        exp = {"pedigree_reg_num": "04107268", "name": "オリオンザドンペリ"}
        self.assertSubDict(exp, act)

    def test_load_trainer(self):
        act = model_to_dict(self.trainer)
        exp = {"name": "小西一男", "code": "10276"}
        self.assertSubDict(exp, act)

    def test_load_jockey(self):
        act = model_to_dict(self.jockey)
        exp = {"name": "内田博幸", "code": "30113"}
        self.assertSubDict(exp, act)

    def test_load_contender(self):
        act = model_to_dict(self.contender)
        exp = {
            "num": 11,
            "order_of_finish": 1,
            "penalty": choices.PENALTY.NORMAL,
            "time": 132.5,
            "mounted_weight": 57.0,
            "odds_win": 14.2,
            "popularity": 6,
            "idm": 59,
            "speed_idx": 55,
            "pace": 3,
            "late_start": None,
            "positioning": None,
            "disadvt": None,
            "b3f_disadvt": None,
            "mid_disadvt": None,
            "f3f_disadvt": None,
            "race_line": choices.RACE_LINE.MIDDLE,
            "improvement": choices.IMPROVEMENT.B,
            "physique": choices.PHYSIQUE.NORMAL,
            "demeanor": choices.DEMEANOR.EXCITED,
            "pace_cat": choices.PACE_CATEGORY.HIGH,
            "b3f_time_idx": 0.8,
            "f3f_time_idx": -10.2,
            "pace_idx": 9.6,
            "margin": 0.3,
            "b3f_time": 35.1,
            "f3f_time": 35.0,
            "odds_show": 2.3,
            "odds_win_10am": 21.5,
            "odds_show_10am": 3.5,
            "c1p": 6,
            "c2p": 7,
            "c3p": 6,
            "c4p": 6,
            "b3f_1p_margin": -0.8,
            "f3f_1p_margin": -0.7,
            "weight": 464,
            "weight_diff": -8,
            "run_style": choices.RUNNING_STYLE.OTP,
            "purse": 740,
            "pace_flow": 8,
            "c4_race_line": choices.RACE_LINE.MIDDLE,
        }

        self.assertSubDict(exp, act)
