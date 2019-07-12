import glob
import logging
from concurrent.futures import as_completed
from concurrent.futures.process import ProcessPoolExecutor

from django.core.management import BaseCommand
from psycopg2.extensions import TransactionRollbackError
from sqlalchemy.exc import OperationalError

from ...templates.template import template_factory, extract_template_name

logger = logging.getLogger(__name__)

TEMPLATES = [
    "BAC",
    "CSA",
    "CYB",
    "CZA",
    "KAB",
    "KSA",
    "KYI",
    "KZA",
    "OT",
    "OU",
    "OV",
    "OW",
    "OZ",
    "SED",
    "SKB",
    "SRB",
    "UKC",
]


def load(path: str) -> str:
    template = template_factory(path)
    template.extract().load()
    return template.path


class Command(BaseCommand):
    help = "Extract, transform and load JRDB file contents into database"

    def __init__(self):
        super().__init__()
        self.error_count = 0
        self.success_count = 0
        self.deadlock_count = 0

    def add_arguments(self, parser):
        parser.add_argument(
            "path", help="A path (can be glob) pointing to the files to import."
        )
        parser.add_argument(
            "-m",
            "--max-workers",
            type=int,
            help="Max number of processes in pool (defaults to number of processors on the machine)",
        )

    def handle(self, *args, **options):
        options_repr = ", ".join(
            [f"{name}: {value}" for name, value in options.items()]
        )
        logger.info(f"START <{options_repr}>")

        attempts = 0
        attempts_max = 3

        pending = [
            path
            for path in glob.glob(options.get("path"))
            if extract_template_name(path) in TEMPLATES
        ]
        pending_len = len(pending)

        with ProcessPoolExecutor(options.get("max_workers")) as executor:
            while len(pending) > 0 and attempts < attempts_max:
                attempts += 1

                futures = {executor.submit(load, path): path for path in pending}

                for future in as_completed(futures):
                    remaining = len(pending)
                    loaded = pending_len - remaining
                    progress = round(loaded / pending_len * 100, 1)

                    path = futures[future]
                    logger.info(
                        f"[{progress}%] ({loaded}/{pending_len}) "
                        f"import <path {path}, attempt {attempts}>"
                    )

                    try:
                        future.result()
                    except (OperationalError, TransactionRollbackError) as e:
                        message = e.args[0].split("\n")[0]
                        logger.info(f"{message} <{path}>")
                        self._increment_deadlock_count()
                    except Exception as e:
                        logger.exception(e)
                        pending.remove(path)
                        self._increment_error_count()
                    else:
                        pending.remove(path)
                        self._increment_success_count()

        logger.info(
            f"FINISH <"
            f"success {self.success_count}, "
            f"unknown errors {self.error_count}, "
            f"deadlocks {self.deadlock_count}, "
            f"attempts {attempts}, "
            f"pending {len(pending)}"
            f">"
        )

    def _increment_error_count(self):
        self.error_count += 1

    def _increment_deadlock_count(self):
        self.deadlock_count += 1

    def _increment_success_count(self):
        self.success_count += 1
