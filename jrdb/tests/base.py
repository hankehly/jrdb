import os

from django.conf import settings
from django.core.management import call_command
from django.test import TransactionTestCase

from jrdb.store import store

SAMPLES_DIR = os.path.join(settings.BASE_DIR, "jrdb", "tests", "samples")


class JRDBTestCase(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if cls.fixtures:
            for db_name in cls._databases_names(include_mirrors=False):
                try:
                    call_command(
                        "loaddata",
                        *cls.fixtures,
                        **{"verbosity": 0, "database": db_name},
                    )
                except Exception:
                    raise

        try:
            cls.setUpTestData()
        except Exception:
            cls._remove_databases_failures()
            raise

    @classmethod
    def setUpTestData(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        store.engine.dispose()

    def assertSubDict(self, sub, sup):
        diff = [key for key in sub if (key in sup and not sup[key] == sub[key])]
        msg = " , ".join(
            [
                f"{key} <"
                f"subset: {sub[key]} ({type(sub[key]).__name__}), "
                f"superset: {sup[key]} ({type(sup[key]).__name__})"
                f">"
                for key in diff
            ]
        )
        return self.assertTrue(sub.items() <= sup.items(), msg)
