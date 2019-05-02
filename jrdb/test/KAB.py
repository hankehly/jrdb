import os

from django.conf import settings
from django.forms import model_to_dict

from jrdb.models import choices, Program
from jrdb.test.base import JRDBTestCase
from jrdb.templates import KAB

TEMPLATE_PATH = os.path.join(settings.BASE_DIR, 'jrdb', 'test', 'samples', 'KAB080913.txt')


class KABTestCase(JRDBTestCase):
    fixtures = ['racetrack']

    @classmethod
    def setUpTestData(cls):
        t = KAB(TEMPLATE_PATH).extract()

        # only import the first row to make
        # test record easy to identify
        t.df = t.df.iloc[0].to_frame().T
        t.load()

        cls.program = Program.objects.first()

    def test_load_program(self):
        act = model_to_dict(self.program)
        exp = {
            'racetrack': 1,
            'yr': 8,
            'round': 2,
            'day': '1',
            'host_category': choices.HOST_CATEGORY.LOCAL,
            'weather': choices.WEATHER.FINE,
            'turf_cond': choices.TRACK_CONDITION_KA.GREAT,
            'turf_cond_inner': choices.TRACK_CONDITION_KA.GOOD,
            'turf_cond_mid': choices.TRACK_CONDITION_KA.GOOD,
            'turf_cond_outer': choices.TRACK_CONDITION_KA.GOOD,
            'turf_speed_shift': -2,
            'hs_speed_shift_innermost': -1,
            'hs_speed_shift_inner': 0,
            'hs_speed_shift_mid': 0,
            'hs_speed_shift_outer': 0,
            'hs_speed_shift_outermost': 0,
            'dirt_cond': choices.TRACK_CONDITION_KA.GREAT,
            'dirt_cond_inner': choices.TRACK_CONDITION_KA.GREAT,
            'dirt_cond_mid': choices.TRACK_CONDITION_KA.GREAT,
            'dirt_cond_outer': choices.TRACK_CONDITION_KA.GREAT,
            'dirt_speed_shift': -7,
            'nth_occurrence': 9,
            'turf_type': choices.TURF_TYPE.WESTERN,
            'grass_height': 14,
            'used_rolling_compactor': False,
            'used_anti_freeze_agent': False,
            'mm_precipitation': 0,
        }
        self.assertSubDict(exp, act)
