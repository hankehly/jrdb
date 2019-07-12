import os

from .base import *

broker_host = os.getenv("BROKER_HOST", "localhost")

CELERY_BROKER_URL = f"redis://{broker_host}:6379"
CELERY_RESULT_BACKEND = f"redis://{broker_host}:6379"
