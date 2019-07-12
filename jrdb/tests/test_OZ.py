import os

from django.forms import model_to_dict

from jrdb.models import Program, Race
from jrdb.tests.base import JRDBTestCase, SAMPLES_DIR
from jrdb.templates import OZ


class OZTestCase(JRDBTestCase):
    fixtures = ["racetrack"]

    @classmethod
    def setUpTestData(cls):
        template_path = os.path.join(SAMPLES_DIR, "OZ020908.txt")
        t = OZ(template_path).extract()

        t.df = t.df.iloc[17].to_frame().T.reset_index(drop=True)
        t.load()

        cls.program = Program.objects.first()
        cls.race = Race.objects.first()

    def test_load_program(self):
        act = model_to_dict(self.program)
        exp = {"racetrack": 4, "yr": 2, "round": 4, "day": "2"}
        self.assertSubDict(exp, act)

    def test_load_race(self):
        act = model_to_dict(self.race)
        exp = {"num": 6, "contender_count": 18}
        self.assertSubDict(exp, act)

    def test_load_race_odds_win(self):
        self.assertEqual(len(self.race.odds_win), 18)
        self.assertEqual(self.race.odds_win[0], 2.3)
        self.assertEqual(self.race.odds_win[9], 19.6)
        self.assertEqual(self.race.odds_win[17], 164.1)

    def test_load_race_odds_show(self):
        self.assertEqual(len(self.race.odds_show), 18)
        self.assertEqual(self.race.odds_show[0], 1.2)
        self.assertEqual(self.race.odds_show[9], 3.6)
        self.assertEqual(self.race.odds_show[17], 24.5)

    def test_load_race_odds_quinella(self):
        self.assertEqual(len(self.race.odds_quinella), 153)
        self.assertEqual(self.race.odds_quinella[0], 88.3)
        self.assertEqual(self.race.odds_quinella[76], 620.5)
        self.assertEqual(self.race.odds_quinella[152], 803.6)
