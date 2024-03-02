import datetime
import time
from celery import shared_task, Celery

from .models import UserData
from .views import send_msg_log, auto_post

app = Celery('task', broker='redis://localhost:6379/0')


@shared_task(queue="emaktab_queue")
def post_req():
    time.sleep(10)
    users = UserData.objects.all()
    if users.count() == 0:
        send_msg_log("No users found")
        return
    for user in users:
        try:
            response = auto_post(user.login, user.password)
            if response:
                user.last_login = datetime.datetime.now()
                user.today_status = True
                send_msg_log(f"✅-{user.login}")
            else:
                send_msg_log(f"🛑-{user.login}")
        except Exception as e:
            send_msg_log(f"Error \n{e}")
