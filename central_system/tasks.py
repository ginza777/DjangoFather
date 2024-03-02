from celery import shared_task, Celery
from central_system.functions import *

app = Celery('task', broker='redis://localhost:6379/0')


@shared_task(queue="backup_database_task")
def backup_database_task():
    backup_database()

@shared_task(queue="webhook_info_task")
def webhook_info_task():
    webhook_info()

@shared_task(queue="set_webhook_task")
def set_webhook_task():
    set_webhook()