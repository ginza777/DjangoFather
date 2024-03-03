import time

from django.core.management.base import BaseCommand
import json
from central_system.models import LogSenderBot, BackupDbBot
from  projects.caption_editor_bot.models import TelegramBot,Channel,Keyword
from projects.chatgpt_bot.models import TelegramBot as ChatGptBot
from projects.emaktabuz.models import ChannelLog
from projects.tarjimon_bot.models import TelegramBot as TarjimonBot


def json_loader(filename):
    with open(f"central_system/management/commands/{filename}", "r") as file:
        return json.loads(file.read())


def add_data_to_bot_db():
    data = json_loader('data.json')
    # LogSenderBot
    token = data["central_system"]["log_sender_bot"]["token"]
    channel_id = data["central_system"]["log_sender_bot"]["channel_id"]
    channel_name = data["central_system"]["log_sender_bot"]["channel_name"]
    if not LogSenderBot.objects.filter(token=token, channel_id=channel_id, channel_name=channel_name).exists():
        LogSenderBot.objects.create(token=token, channel_id=channel_id, channel_name=channel_name)
    # BackupDbBot
    token = data["central_system"]["backup_bot"]["token"]
    channel_id = data["central_system"]["backup_bot"]["channel_id"]
    channel_name = data["central_system"]["backup_bot"]["channel_name"]
    if not BackupDbBot.objects.filter(token=token, channel_id=channel_id, channel_name=channel_name).exists():
        BackupDbBot.objects.create(token=token, channel_id=channel_id, channel_name=channel_name)
    # TelegramBot
    token = data["central_system"]["caption_editor_bot"]["bot"]["token"]
    if not TelegramBot.objects.filter(bot_token=token).exists():
        TelegramBot.objects.create(bot_token=token)
    # Channel
    for channel_data in data["central_system"]["caption_editor_bot"]["channels"]:
        channel_id = channel_data["channel_id"]
        channel_name = channel_data["name"]
        channel_link = channel_data["link"]
        # Channel ni tekshirish
        if not Channel.objects.filter(channel_id=channel_id, name=channel_name, channel_sign=channel_link).exists():
            # Channel ni yaratish
            channel = Channel.objects.create(channel_id=channel_id, name=channel_name, channel_sign=channel_link)
            # Kanalga teglar (keywords)ni qo'shish
            if "keywords" in channel_data:
                keywords = channel_data["keywords"]
                for keyword in keywords:
                    # Keywordni tekshirish
                    if not Keyword.objects.filter(channel=channel, text=keyword).exists():
                        Keyword.objects.create(channel=channel, text=keyword)
    # ChatGptBot
    bot_list = data["central_system"]["chatgpt_bot"]
    for token in bot_list:
        # Botni tekshirish
        if not ChatGptBot.objects.filter(bot_token=token).exists():
            ChatGptBot.objects.create(bot_token=token)
            time.sleep(1)
    # ChannelLog
    channel = data["central_system"]["emaktabuz_bot"]
    # ChannelLog ni tekshirish
    if not ChannelLog.objects.filter(channel_id=channel["channel_id"], channel_name=channel["channel_name"], bot_token=channel["token"]).exists():
        ChannelLog.objects.create(
            channel_id=channel["channel_id"],
            channel_name=channel["channel_name"],
            bot_token=channel["token"]
        )
    # TarjimonBot
    bot_list = data["central_system"]["tarjimon_bot"]
    for token in bot_list:
        # Botni tekshirish
        if not TarjimonBot.objects.filter(bot_token=token).exists():
            TarjimonBot.objects.create(bot_token=token)
            time.sleep(1)

class Command(BaseCommand):
    help = "fill the database with the default values"

    def handle(self, *args, **options):
        add_data_to_bot_db()

