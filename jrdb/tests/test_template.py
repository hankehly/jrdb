import os

from jrdb.models import Race
from jrdb.templates import BAC
from jrdb.tests.base import JRDBTestCase, SAMPLES_DIR


class TemplateTestCase(JRDBTestCase):
    fixtures = ["racetrack"]

    def test_created_record_count_equals_template_row_count(self):
        template_path = os.path.join(SAMPLES_DIR, "BAC080913.txt")
        t = BAC(template_path).extract()
        t.load()

        exp_count = len(t.df.index)
        act_count = Race.objects.count()

        self.assertEqual(act_count, exp_count)

    def test_before_after_update_record_count(self):
        template_path = os.path.join(SAMPLES_DIR, "BAC080913.txt")
        t = BAC(template_path).extract()

        t.load()
        t.load()

        exp_count = len(t.df.index)
        act_count = Race.objects.count()

        self.assertEqual(act_count, exp_count)
