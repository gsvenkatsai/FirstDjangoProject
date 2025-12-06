import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE','project1.settings.dev')
celery = Celery('project1')
celery.config_from_object('django.conf:settings',namespace='CELERY')
celery.autodiscover_tasks()