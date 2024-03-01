import uuid

import requests

from .models import LogSenderBot


def send_msg_log(message):
    # Define maximum length for each message chunk
    max_length = 4096

    if LogSenderBot.objects.all().count() > 0:
        token = LogSenderBot.objects.last().token
    else:
        token = "7121286690:AAGCEKeBvUKKb_K5kkaXnruJq2BAOVUg3-k"
    chat_id = -1002126638542

    # Split the message into chunks
    message_chunks = [message[i:i + max_length] for i in range(0, len(message), max_length)]

    for chunk in message_chunks:
        # Format the chunk as code (HTML-style markdown)
        formatted_chunk = f"<code>{chunk}</code>"

        url = f'https://api.telegram.org/bot{token}/sendMessage'
        params = {
            'chat_id': chat_id,
            'text': formatted_chunk,
            'parse_mode': 'HTML'
        }
        r = requests.post(url, data=params)
        if r.status_code != 200:
            return False
    return True


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
