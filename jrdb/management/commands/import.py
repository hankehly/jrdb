import glob
import logging
import os
import re
from concurrent.futures import as_completed
from concurrent.futures.process import ProcessPoolExecutor

from django.core.management import BaseCommand, CommandError
from django.db import OperationalError
from django.utils.module_loading import import_string
from psycopg2.extensions import TransactionRollbackError

logger = logging.getLogger(__name__)

TEMPLATES = [
    'BAC',
    'CSA', 'CYB', 'CZA',
    'KAB', 'KSA', 'KYI', 'KZA',
    'OT', 'OU', 'OV', 'OW', 'OZ',
    'SED', 'SKB', 'SRB',
    'UKC'
]


def extract_template_name(path: str):
    basename = os.path.basename(path)
    filename, _ = os.path.splitext(basename)
    return re.search('[A-Z]+', filename).group()


def load(path: str) -> str:
    template = extract_template_name(path)
    module_path = '.'.join(['jrdb', 'templates', template])
    parser = import_string(module_path)(path)
    parser.extract().load()
    return parser.path


class Command(BaseCommand):
    help = 'Extract, transform and load JRDB file contents into database'

    def __init__(self):
        super().__init__()
        self.error_count = 0
        self.success_count = 0

    def add_arguments(self, parser):
        parser.add_argument('path', help='A path (can be glob) pointing to the files to import.')
        parser.add_argument('-m', '--max-workers', type=int,
                            help='Max number of processes in pool (defaults to number of processors on the machine)')

    def handle(self, *args, **options):
        options_pretty = ', '.join([f'{name}: {value}' for name, value in options.items()])
        logger.info(f"START <{options_pretty}>")

        attempts = 0
        max_attempts = 3
        pending_load = glob.glob(options.get('path'))

        with ProcessPoolExecutor(options.get('max_workers')) as executor:
            while len(pending_load) > 0 and attempts < max_attempts:
                attempts += 1

                futures = {
                    executor.submit(load, path): path for path in pending_load
                    if extract_template_name(path) in TEMPLATES
                }

                for future in as_completed(futures):
                    path = futures[future]
                    logger.info(f'import <path {path}, attempt {attempts}>')
                    try:
                        future.result()
                    except (OperationalError, TransactionRollbackError) as e:
                        message = e.args[0].split('\n')[0]
                        logger.info(f'{message} <{path}>')
                    except Exception as e:
                        logger.exception(e)
                        pending_load.remove(path)
                        self._increment_error_count()
                    else:
                        pending_load.remove(path)
                        self._increment_success_count()

        logger.info(
            f'FINISH <'
            f'success {self.success_count}, '
            f'unknown errors {self.error_count}, '
            f'attempts {attempts}, '
            f'unhandled (unable to load after {max_attempts} attempts) {len(pending_load)}'
            f'>'
        )

    def _increment_error_count(self):
        self.error_count += 1

    def _increment_success_count(self):
        self.success_count += 1
