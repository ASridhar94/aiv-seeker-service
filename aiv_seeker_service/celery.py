from __future__ import absolute_import, unicode_literals

import os
import sys

from celery.signals import after_setup_logger
import logging

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aiv_seeker_service.settings')

app = Celery('aiv_seeker_service')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@after_setup_logger.connect()
def logger_setup_handler(logger, **kwargs):
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # custom formatter
    handler.setFormatter(formatter)
    logger.addHandler(handler)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
