import os
import environ
from celery import Celery
from django.conf import settings

# Load environment variables from .env file
env = environ.Env()
environ.Env.read_env()

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Create a Celery instance
app = Celery("core")

# Configure Celery using Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
