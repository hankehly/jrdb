import glob
import logging

from celery import group
from django.core.management import BaseCommand

from ...tasks import import_file
from ...templates.template import extract_template_name

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


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "path", help="A path (can be glob) pointing to the files to import."
        )

    def handle(self, *args, **options):
        option_strings = [f"{name}: {value}" for name, value in options.items()]
        options_repr = ", ".join(option_strings)

        logger.info(f"START <{options_repr}>")

        paths = glob.glob(options.get("path"))
        pending = [p for p in paths if extract_template_name(p) in TEMPLATES]

        task_signatures = (import_file.s(path) for path in pending)
        results = group(task_signatures)()

        results.get()

        logger.info("FINISH")
