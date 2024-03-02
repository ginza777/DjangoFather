import datetime

from celery import shared_task, Celery



app = Celery('task', broker='redis://localhost:6379/0')


@shared_task(queue="emaktab_queue")
def post_req():
    pass