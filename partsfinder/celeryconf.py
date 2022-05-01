import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# from django.apps import apps
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "partsfinder.settings")

app = Celery("partsfinder")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
app.conf.beat_schedule = {
    "crawl_data": {
        "task": "core.products.tasks.crawl_data",
        "schedule": crontab(minute="*/1"),
    },
}
