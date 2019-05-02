import os

from django.conf import settings
from django.forms import model_to_dict

from jrdb.models import choices, Contender, Program, Race
from jrdb.test.base import JRDBTestCase
from jrdb.templates import CYB

TEMPLATE_PATH = os.path.join(settings.BASE_DIR, 'jrdb', 'test', 'samples', 'CYB081018.txt')


class CYBTestCase(JRDBTestCase):
    fixtures = ['racetrack']

    @classmethod
    def setUpTestData(cls):
        t = CYB(TEMPLATE_PATH).extract()

        # only import the first row to make
        # test record easy to identify
        t.df = t.df.iloc[0].to_frame().T
        t.load()

        cls.program = Program.objects.first()
        cls.race = Race.objects.first()
        cls.contender = Contender.objects.first()

    def test_load_program(self):
        act = model_to_dict(self.program)
        exp = {'racetrack': 5, 'yr': 8, 'round': 4, 'day': '3'}
        self.assertSubDict(exp, act)

    def test_load_race(self):
        act = model_to_dict(self.race)
        exp = {'num': 1}
        self.assertSubDict(exp, act)

    def test_load_contender(self):
        act = model_to_dict(self.contender)

        exp = {
            'num': 1,
            'training_style': '04',
            'training_course_cat': '3',
            'trained_hill': True,
            'trained_wood_chip': False,
            'trained_dirt': False,
            'trained_turf': False,
            'trained_pool': False,
            'trained_obstacle': False,
            'trained_poly_track': True,
            'training_distance': choices.TRAINING_DISTANCE.LONG,
            'training_emphasis': choices.TRAINING_EMPHASIS.AVG,
            'warm_up_time_idx': 56,
            'training_result_idx': 56,
            'training_amount_eval': choices.TRAINING_AMOUNT_EVAL.NORMAL,
            'training_result_idx_change': choices.TRAINING_RESULT_IDX_CHANGE.BOLSTER,
            'training_comment': None,
            'training_comment_date': None,
            'training_evaluation': None,
        }

        self.assertSubDict(exp, act)
