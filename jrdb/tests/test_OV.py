import os

from django.conf import settings
from django.forms import model_to_dict

from jrdb.models import Program, Race
from jrdb.tests.base import JRDBTestCase
from jrdb.templates import OV

TEMPLATE_PATH = os.path.join(settings.BASE_DIR, 'jrdb', 'tests', 'samples', 'OV040828.txt')


class OVTestCase(JRDBTestCase):
    fixtures = ['racetrack']

    @classmethod
    def setUpTestData(cls):
        t = OV(TEMPLATE_PATH).extract()

        # only import the first row to make
        # test record easy to identify
        t.df = t.df.iloc[0].to_frame().T
        t.load()

        cls.program = Program.objects.first()
        cls.race = Race.objects.first()

    def test_load_program(self):
        act = model_to_dict(self.program)
        exp = {'racetrack': 1, 'yr': 4, 'round': 1, 'day': '5'}
        self.assertSubDict(exp, act)

    def test_load_race(self):
        act = model_to_dict(self.race)
        exp = {'num': 1, 'contender_count': 10}
        self.assertSubDict(exp, act)

        self.assertEqual(len(self.race.odds_trifecta), 4896)
        self.assertEqual(self.race.odds_trifecta[0], 245.5)
        self.assertEqual(self.race.odds_trifecta[2448], 967.3)
        self.assertEqual(self.race.odds_trifecta[4895], None)
