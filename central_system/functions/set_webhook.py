import environ
import requests
import time

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
    caption_editor_bots = CaptionEditorBot.objects.all()
    chatgpt_bots = ChatGPTBot.objects.all()
    tarjimon_bots = TarjimonBot.objects.all()
    bots.append(caption_editor_bots)
    bots.append(chatgpt_bots)
    bots.append(tarjimon_bots)
    return bots


def set_webhook_single(bot_token):
    webhook_url = bot_webhook_url
    url = (
        f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}/bot/handle_telegram_webhook/{bot_token}"
    )
    response = requests.post(url)
    return response.json()

def set_webhook():
    bots = get_bot_lists()
    for bot in bots:
        res=set_webhook_single(bot.bot_token)
        send_msg_log(f"Webhook set for bot:\n {res}")
        time.sleep(1)
    return True

__all__ = ["set_webhook"]