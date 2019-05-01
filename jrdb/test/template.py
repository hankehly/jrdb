import os

from django.conf import settings

from jrdb.models import Race
from jrdb.templates import BAC
from jrdb.test.base import JRDBTestCase

TEMPLATE_PATH = os.path.join(settings.BASE_DIR, 'jrdb', 'test', 'samples', 'BAC080913.txt')


class TemplateTestCase(JRDBTestCase):
    fixtures = ['racetrack']

    def test_created_record_count_equals_template_row_count(self):
        t = BAC(TEMPLATE_PATH).extract()
        t.load()

        exp_count = len(t.df.index)
        act_count = Race.objects.count()

        self.assertEqual(act_count, exp_count)

    def test_before_after_update_record_count(self):
        t = BAC(TEMPLATE_PATH).extract()

        t.load()
        t.load()

        exp_count = len(t.df.index)
        act_count = Race.objects.count()

        self.assertEqual(act_count, exp_count)
