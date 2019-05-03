import os

from django.conf import settings
from django.forms import model_to_dict

from jrdb.models import Program, Race
from jrdb.tests.base import JRDBTestCase
from jrdb.templates import OU

TEMPLATE_PATH = os.path.join(settings.BASE_DIR, 'jrdb', 'tests', 'samples', 'OU020908.txt')


class OUTestCase(JRDBTestCase):
    fixtures = ['racetrack']

    @classmethod
    def setUpTestData(cls):
        t = OU(TEMPLATE_PATH).extract()

        # only import the first row to make
        # test record easy to identify
        t.df = t.df.iloc[0].to_frame().T
        t.load()

        cls.program = Program.objects.first()
        cls.race = Race.objects.first()

    def test_load_program(self):
        act = model_to_dict(self.program)
        exp = {'racetrack': 1, 'yr': 2, 'round': 2, 'day': '2'}
        self.assertSubDict(exp, act)

    def test_load_race(self):
        act = model_to_dict(self.race)
        exp = {'num': 1, 'contender_count': 13}
        self.assertSubDict(exp, act)

        self.assertEqual(len(self.race.odds_exacta), 306)
        self.assertEqual(self.race.odds_exacta[0], 57.8)
        self.assertEqual(self.race.odds_exacta[153], 317.9)
        self.assertEqual(self.race.odds_exacta[305], None)
