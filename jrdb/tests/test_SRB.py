import os

from django.conf import settings
from django.forms import model_to_dict

from jrdb.models import Program, Race
from jrdb.tests.base import JRDBTestCase
from jrdb.templates import SRB

TEMPLATE_PATH = os.path.join(settings.BASE_DIR, 'jrdb', 'tests', 'samples', 'SRB080913.txt')


class SRBTestCase(JRDBTestCase):
    fixtures = ['racetrack']

    @classmethod
    def setUpTestData(cls):
        t = SRB(TEMPLATE_PATH).extract()

        # only import the first row to make
        # test record easy to identify
        t.df = t.df.iloc[0].to_frame().T
        t.load()

        cls.program = Program.objects.first()
        cls.race = Race.objects.first()

    def test_load_program(self):
        act = model_to_dict(self.program)
        exp = {
            'racetrack': 1,
            'yr': 8,
            'round': 2,
            'day': '1',
        }
        self.assertSubDict(exp, act)

    def test_load_race(self):
        act = model_to_dict(self.race)
        exp = {
            'num': 1,
            'c1_track_bias': [None, None, None],
            'c2_track_bias': [None, None, None],
            'bs_track_bias': [2, 4, 3],
            'c3_track_bias': [2, 4, 3],
            'c4_track_bias': [2, 4, 4, 3, 3],
            'hs_track_bias': [2, 4, 4, 3, 3],
            'comment': (
                '多分当日馬場叩きなど入れてると思うが、明らかに芝1200mはラチ沿い有利＋大外回し不利。かなり内枠有利も見受けられた。'
                '向こう正面からして踏み固められてる部分の方が良い。'
            ),
        }
        self.assertSubDict(exp, act)
