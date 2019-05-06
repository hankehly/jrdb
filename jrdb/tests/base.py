import os

from django.conf import settings
from django.test import TestCase

SAMPLES_DIR = os.path.join(settings.BASE_DIR, 'jrdb', 'tests', 'samples')


class JRDBTestCase(TestCase):

    def assertSubDict(self, sub, sup):
        diff = [key for key in sub if (key in sup and not sup[key] == sub[key])]
        msg = ' , '.join([
            f'{key} <'
            f'subset: {sub[key]} ({type(sub[key]).__name__}), '
            f'superset: {sup[key]} ({type(sup[key]).__name__})'
            f'>' for key in diff
        ])
        return self.assertTrue(sub.items() <= sup.items(), msg)
