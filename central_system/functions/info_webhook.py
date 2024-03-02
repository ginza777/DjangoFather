import time

import environ
import requests

from central_system.views import send_msg_log
#all telegram bots
from projects.caption_editor_bot.models import TelegramBot as CaptionEditorBot
from projects.chatgpt_bot.models import TelegramBot as ChatGPTBot
from projects.tarjimon_bot.models import TelegramBot as TarjimonBot

env = environ.Env()
env.read_env(".env")

bot_webhook_url = env.str("WEBHOOK_URL")

def get_bot_lists():
    bots = []
    caption_editor_bots = CaptionEditorBot.objects.all()
    chatgpt_bots = ChatGPTBot.objects.all()
    tarjimon_bots = TarjimonBot.objects.all()
    bots.append(caption_editor_bots)
    bots.append(chatgpt_bots)
    bots.append(tarjimon_bots)
    return bots
def webhook_info():
    bots = get_bot_lists()
    for bot in bots:
        url = f"https://api.telegram.org/bot{bot.bot_token}/getWebhookInfo"
        response = requests.post(url)
        send_msg_log(f"Webhook info for bot:\n {response.json()}")
        time.sleep(1)


__all__ = ["webhook_info"]