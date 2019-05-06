import datetime
import os

import pytz
from django.forms import model_to_dict

from jrdb.models import Program, Race, choices
from jrdb.tests.base import JRDBTestCase, SAMPLES_DIR
from jrdb.templates import BAC


class BACTestCase(JRDBTestCase):
    fixtures = ['racetrack', 'race_condition_code']

    @classmethod
    def setUpTestData(cls):
        template_path = os.path.join(SAMPLES_DIR, 'BAC080913.txt')
        t = BAC(template_path).extract()

        # only import the first row to make
        # test record easy to identify
        t.df = t.df.iloc[0].to_frame().T
        t.load()

        cls.program = Program.objects.first()
        cls.race = Race.objects.first()

    def test_load_program(self):
        act = model_to_dict(self.program)
        exp = {'racetrack': 1, 'yr': 8, 'round': 2, 'day': '1'}
        self.assertSubDict(exp, act)

    def test_load_race(self):
        act = model_to_dict(self.race)

        exp = {
            'num': 1,
            'started_at': pytz.timezone('Asia/Tokyo').localize(datetime.datetime(2008, 9, 13, 10, 0)),
            'distance': 1200,
            'surface': choices.SURFACE.TURF,
            'direction': choices.DIRECTION.RIGHT,
            'course_inout': choices.COURSE_INOUT.INSIDE,
            'category': choices.RACE_CATEGORY.TWO_YR_OLD,
            'cond': 10,
            'horse_type_symbol': choices.RACE_HORSE_TYPE_SYMBOL.MIX,
            'horse_sex_symbol': choices.RACE_HORSE_SEX_SYMBOL.NA,
            'interleague_symbol': choices.RACE_INTERLEAGUE_SYMBOL.DES,
            'impost_class': choices.IMPOST_CLASS.WEIGHT_FOR_AGE,
            'grade': None,
            'name': None,
            'nth_occurrence': None,
            'contender_count': 8,
            'course_label': choices.COURSE_LABEL.A,
            'host_category': choices.HOST_CATEGORY.LOCAL,
            'name_abbr': None,
            'name_short': '２歳未勝利',
            'p1_purse': 500,
            'p2_purse': 200,
            'p3_purse': 130,
            'p4_purse': 75,
            'p5_purse': 50,
            'p1_prize': 400,
            'p2_prize': 0,
            'sold_win': True,
            'sold_show': True,
            'sold_bracket_quinella': False,
            'sold_quinella': True,
            'sold_exacta': True,
            'sold_duet': True,
            'sold_trio': True,
            'sold_trifecta': True,
            'win5': None,
        }

        self.assertSubDict(exp, act)
