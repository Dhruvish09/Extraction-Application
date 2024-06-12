# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'text_extraction_service.settings')

app = Celery('text_extraction_service')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-failed-upload-emails': {
        'task': 'extraction.tasks.send-failed-upload-emails',  # Adjust the task path based on your project structure
        'schedule': crontab(minute=0, hour='*/3'),  # Adjust the schedule as needed (e.g., every 3 hours)
    },
}
