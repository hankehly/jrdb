import glob
import logging
import os
import re
from concurrent.futures import as_completed
from concurrent.futures.process import ProcessPoolExecutor

from django.core.management import BaseCommand
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


def get_template_name(path: str):
    basename = os.path.basename(path)
    filename, _ = os.path.splitext(basename)
    return re.search('[A-Z]+', filename).group()


def load(path: str) -> str:
    template = get_template_name(path)
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

        self._failed = []
        self._retries = 0

    def add_arguments(self, parser):
        parser.add_argument('path', help='A path (can be glob) pointing to the files to import.')
        parser.add_argument('-m', '--max-workers', type=int,
                            help='Max number of processes in pool (defaults to number of processors on the machine)')

    def handle(self, *args, **options):
        options_str = ', '.join([f'{name}: {value}' for name, value in options.items()])
        logger.info(f"START <{options_str}>")

        with ProcessPoolExecutor(max_workers=options.get('max_workers')) as executor:
            futures = {
                executor.submit(load, path): path for path in glob.iglob(options['path'])
                if get_template_name(path) in TEMPLATES
            }

            for future in as_completed(futures):
                path = futures[future]
                try:
                    logger.info(f'import <{path}>')
                    future.result()
                    self._increment_success_count()
                except (OperationalError, TransactionRollbackError):
                    logger.info(f'marking for retry <{path}>')
                    self._failed.append(path)
                except Exception as e:
                    logger.exception(e)
                    self._increment_error_count()

            logger.info(f'>>> RETRIES <<<')

            while len(self._failed) > 0 and self._retries < 3:
                retries = {executor.submit(load, path): path for path in self._failed}
                for future in as_completed(retries):
                    path = retries[future]
                    try:
                        logger.info(f'retry <{path}>')
                        future.result()
                    except Exception as e:
                        logger.exception(e)
                        continue
                    else:
                        ix = self._failed.index(path)
                        self._failed.pop(ix)

        logger.info(f'FINISH <successful {self.success_count}, errors {self.error_count}>')

    def _increment_error_count(self):
        self.error_count += 1

    def _increment_success_count(self):
        self.success_count += 1
