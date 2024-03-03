import os
import environ
from celery import Celery
from django.conf import settings

# Load environment variables from .env file
env = environ.Env()
env.read_env(".env")

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Initialize Django settings
if not settings.configured:
    settings.configure()

# Create a Celery instance
app = Celery("core")
app.conf.enable_utc = False

# Autodiscover tasks
app.autodiscover_tasks()

# Configure Celery with Django settings
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
