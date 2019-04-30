import glob
import logging
import os
import re
from concurrent.futures import as_completed
from concurrent.futures.process import ProcessPoolExecutor

from django.core.management import BaseCommand
from django.utils.module_loading import import_string

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


def import_document(path: str) -> str:
    template = get_template_name(path)
    module_path = '.'.join(['jrdb', 'templates', template])
    parser = import_string(module_path)(path)
    parser.extract().load()
    return parser.path


class Command(BaseCommand):
    help = 'Import 1 or more JRDB data files of the same type'

    def __init__(self):
        super().__init__()

        self.error_count = 0
        self.success_count = 0

    def add_arguments(self, parser):
        parser.add_argument('path', help='A path (can be glob) pointing to the files to import.')
        parser.add_argument('--workers', type=int,
                            help='Number of processes in pool (defaults to the number of processors on the machine)')

    def handle(self, *args, **options):
        options_str = ', '.join([f'{name}: {value}' for name, value in options.items()])
        logger.info(f"START <{options_str}>")

        with ProcessPoolExecutor(max_workers=options.get('workers')) as executor:
            futures = {
                executor.submit(import_document, path): path
                for path in glob.iglob(options['path'])
                if get_template_name(path) in TEMPLATES
            }

            for future in as_completed(futures):
                path = futures[future]
                try:
                    logger.info(f'import <{path}>')
                    future.result()
                except Exception as e:
                    logger.exception(e)
                    self._increment_error_count()
                else:
                    self._increment_success_count()

        logger.info(f'FINISH <successful {self.success_count}, errors {self.error_count}>')

    def _increment_error_count(self):
        self.error_count += 1

    def _increment_success_count(self):
        self.success_count += 1
