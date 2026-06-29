import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zecser_project.settings')

app = Celery('zecser_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()