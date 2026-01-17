import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backendSvc.settings")

app = Celery('backendSvc')

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()