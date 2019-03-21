import glob
import logging
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

from django.core.management import BaseCommand
from django.utils.module_loading import import_string

from jrdb.templates.template import Template

logger = logging.getLogger(__name__)


def import_document(parser: Template) -> str:
    parser.parse().persist()
    return parser.filepath


class Command(BaseCommand):
    help = 'Import 1 or more JRDB data files of the same type'

    def __init__(self):
        super().__init__()

        self.error_count = 0
        self.success_count = 0

    def add_arguments(self, parser):
        parser.add_argument('template', choices=['BAC', 'CSA', 'CZA', 'KSA', 'KZA', 'SED', 'SRB', 'UKC'],
                            help='Template parser used during import.')
        parser.add_argument('path', help='A path (can be glob) pointing to the files to import.')
        parser.add_argument('--threads', type=int, help='Threads to use during processing (default is 1)', default=1)

    def handle(self, *args, **options):
        logger.info(f"START <template: {options['template']}, path: {options['path']}, threads: {options['threads']}>")

        if options['threads'] > 1:
            self._process_multi_thread(options)
        else:
            self._process_single_thread(options)

        logger.info(f'FINISH <successful {self.success_count}, errors {self.error_count}>')

    def _process_multi_thread(self, options: dict):
        module_path = '.'.join(['jrdb', 'templates', options['template']])
        parser_cls = import_string(module_path)

        with ThreadPoolExecutor(max_workers=options['threads']) as executor:
            futures = {
                executor.submit(import_document, parser_cls(path)) for path in glob.iglob(options['path'])
            }

            for future in as_completed(futures):
                try:
                    path = future.result()
                except ValueError as e:
                    logger.exception(e)
                    self._increment_error_count()
                else:
                    logger.info(f'import success <{path}>')
                    self._increment_success_count()

    def _process_single_thread(self, options: dict):
        module_path = '.'.join(['jrdb', 'templates', options['template']])
        parser_cls = import_string(module_path)

        for path in glob.iglob(options['path']):
            try:
                import_document(parser_cls(path))
            except ValueError as e:
                logger.exception(e)
                self._increment_error_count()
            else:
                logger.info(f'import success <{path}>')
                self._increment_success_count()

    def _increment_error_count(self):
        self.error_count += 1

    def _increment_success_count(self):
        self.success_count += 1
