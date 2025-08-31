import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")

app = Celery("alx_backend_graphql_crm", broker="redis://localhost:6379/0")

# Load custom config from Django settings, using CELERY_ namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed apps
app.autodiscover_tasks()
