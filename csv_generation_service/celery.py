"""Celery config."""
import os

from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'csv_generation_service.settings'
)

app = Celery('csv_generation_service')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    BROKER_URL=os.environ['REDIS_URL'],
    CELERY_RESULT_BACKEND=os.environ['REDIS_URL']
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
