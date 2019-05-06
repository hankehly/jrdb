import os

from django.forms import model_to_dict

from jrdb.models import Program, Race
from jrdb.tests.base import JRDBTestCase, SAMPLES_DIR
from jrdb.templates import OW


class OWTestCase(JRDBTestCase):
    fixtures = ['racetrack']

    @classmethod
    def setUpTestData(cls):
        template_path = os.path.join(SAMPLES_DIR, 'OW020908.txt')
        t = OW(template_path).extract()
        t.df = t.df.iloc[0].to_frame().T
        t.load()

    def test_load_program(self):
        program = Program.objects.first()
        act = model_to_dict(program)
        exp = {'racetrack': 1, 'yr': 2, 'round': 2, 'day': '2'}
        self.assertSubDict(exp, act)

    def test_load_race(self):
        race = Race.objects.first()
        act = model_to_dict(race)
        exp = {'num': 1, 'contender_count': 13}
        self.assertSubDict(exp, act)

        self.assertEqual(len(race.odds_duet), 153)
        self.assertEqual(race.odds_duet[0], 10.9)
        self.assertEqual(race.odds_duet[76], 4.5)
        self.assertEqual(race.odds_duet[152], None)
