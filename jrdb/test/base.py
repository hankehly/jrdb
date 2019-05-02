from django.test import TestCase


class JRDBTestCase(TestCase):

    def assertSubDict(self, sub, sup):
        diff = [key for key in sub if (key in sup and not sup[key] == sub[key])]
        msg = ' , '.join([f"{key} <subset: {sub[key]}, superset: {sup[key]}>" for key in diff])
        return self.assertTrue(sub.items() <= sup.items(), msg)
