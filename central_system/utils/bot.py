import requests
from django.conf import settings
from telegram.ext import Application

appname = "chatgpt-bot"


def get_info(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.post(url)
    print(response.json())
    return response.json().get("result").get("username"), response.json().get("result").get("first_name")
