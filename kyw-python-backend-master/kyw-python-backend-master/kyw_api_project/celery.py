import os
from celery import Celery
from decouple import config

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kyw_api_project.settings")


CELERY_BROKER_URL = config("CELERY_BROKER_URL")
app = Celery("kyw_api_project", broker=CELERY_BROKER_URL)
# broker="amqp://admin:mypass@rabbitmq:5672//


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


# Load task modules from all registered Django app configs.
# app.conf.timezone = "UTC"
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#    'add-every-15-seconds': {
#        'task': 'opscentre_usermanagement_api.tasks.update_dashboard_cache',
#        'schedule': 15.0
#    },
# }
