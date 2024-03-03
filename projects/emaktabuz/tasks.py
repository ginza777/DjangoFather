import datetime
import time

from celery import shared_task, Celery

from .models import UserData
from .views import auto_post, emaktab_msg_send_log_to_channel

app = Celery('task', broker='redis://localhost:6379/0')


@shared_task()
def post_req():
    users = UserData.objects.all()
    if users.count() == 0:
        emaktab_msg_send_log_to_channel("emaktabuz:\nNo users found")
        return
    i = 0
    emaktab_msg_send_log_to_channel(f"emaktabuz:\nAuto post started date: {datetime.datetime.now()}")
    for user in users:
        try:
            response = auto_post(user.login, user.password, i)
            if response:
                user.last_login = datetime.datetime.now()
                user.today_status = True
                user.save()

        except Exception as e:
            emaktab_msg_send_log_to_channel(f"Error \n{e}")
        i += 1
        time.sleep(3)
    emaktab_msg_send_log_to_channel(f"-✅--✅--✅--✅--✅--✅--✅--✅-")
