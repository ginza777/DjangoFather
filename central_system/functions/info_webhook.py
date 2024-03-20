import time

import environ
import requests

from central_system.views import send_msg_log
# all telegram bots
from projects.caption_editor_bot.models import TelegramBot as CaptionEditorBot
from projects.chatgpt_bot.models import TelegramBot as ChatGPTBot
from projects.tarjimon_bot.models import TelegramBot as TarjimonBot

env = environ.Env()
env.read_env(".env")

bot_webhook_url = env.str("WEBHOOK_URL")


def get_bot_lists():
    bots = []
    caption_editor_bots = CaptionEditorBot.objects.values_list("bot_token", flat=True)
    chatgpt_bots = ChatGPTBot.objects.values_list("bot_token", flat=True)
    tarjimon_bots = TarjimonBot.objects.values_list("bot_token", flat=True)
    # add all bots to list
    bots.extend(caption_editor_bots)
    bots.extend(chatgpt_bots)
    bots.extend(tarjimon_bots)
    return bots


def webhook_info():
    bots = get_bot_lists()
    message = 'Getting webhook info for all bots...\n'
    message += f'bot count: {len(bots)}\n'

    for bot in bots:
        url = f"https://api.telegram.org/bot{bot}/getWebhookInfo"
        response = requests.post(url)
        if response.status_code == 200:
            message += f"200 - {bot}\n"
            message += f"{response.json()}\n"
        else:
            message += f"{response.status_code} - {bot}\n"
            message += f"{response.json()}\n"
        time.sleep(0.2)
    send_msg_log(message)
__all__ = ["webhook_info"]
