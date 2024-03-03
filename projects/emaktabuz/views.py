import uuid
import requests
from central_system.views import send_msg_log
from .models import ChannelLog



def emaktab_msg_send_log_to_channel(message):
    if ChannelLog.objects.all().count() > 0:
        token = ChannelLog.objects.last().bot_token
        channel_id = ChannelLog.objects.last().channel_id
    else:
        send_msg_log(message)
        send_msg_log("emaktabuz da kanalga xabar jo'natishda xatolik yuz berdi.emaktab__msg_send_log_to_channel funksiyasida Log uchun token va channel_id topilmadi.")
        return

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    params = {
        'chat_id': channel_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        return False

    return True


def auto_post(user_login, user_pass,i):
    url = "https://login.emaktab.uz/login"
    captcha = str(uuid.uuid4())
    data = {
        "exceededAttempts": "False",
        "ReturnUrl": "",
        "FingerprintId": "",
        "login": {user_login},
        "password": {user_pass},
        "Captcha.Input": {captcha},
        "Captcha.Id": id
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        message=f"{i}-✅-{user_login},\n{user_pass}\ntizimga muvaffaqiyatli kirildi"
        emaktab_msg_send_log_to_channel(message)
        return True
    else:
        message=f"{i}-❌-{user_login},\n{user_pass}\ntizimga kirishda xatolik yuz berdi"
        emaktab_msg_send_log_to_channel(message+" \n"+str(response.status_code)+"\n "+str(response.text))
        return False
