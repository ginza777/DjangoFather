import uuid

import requests

from central_system.views import send_msg_log


def auto_post(user_login, user_pass):
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
        send_msg_log("So'rov muvaffaqiyatli jo'natildi.")
        print("So'rov muvaffaqiyatli jo'natildi.")

        return True
    else:
        send_msg_log(f"Xatolik yuz berdi:{response.status_code}")
        print("Xatolik yuz berdi:", response.status_code)
        return False
