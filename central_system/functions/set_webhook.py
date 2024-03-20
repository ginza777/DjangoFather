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


def set_webhook_single(bot_token):
    webhook_url = bot_webhook_url
    url = (
        f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}/bot/handle_telegram_webhook/{bot_token}"
    )
    response = requests.post(url)
    return response


def set_webhook():
    bots = get_bot_lists()
    message = 'Setting webhook for all bots...\n'
    message += f'webhook url: {bot_webhook_url}\n'
    message += f'bot count: {len(bots)}\n'

    for bot in bots:
        res = set_webhook_single(bot)
        if res.status_code == 200:
            message += f"200 - {bot}\n"
        else:
            message += f"{res.status_code} - {bot}\n"
            message += f"{res.json()}\n"
    send_msg_log(message)
    return True


__all__ = ["set_webhook"]
