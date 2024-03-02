import json
import logging

logger = logging.getLogger(__name__)
from django.core.management.base import BaseCommand

from ...models import Bot, Channel_type, Channels, Client_Settings, KeywordChannelAds


# user_data.json
# channel_type.json
# client.json
# channels.json
# keyword.json
#this directory



def json_loader(filename):
    with open(f"projects/telegram_post_scrapper/management/commands/json/{filename}", "r") as file:
        return json.loads(file.read())


def add_data_to_bot_db(data, model):
    for item in data:
        fields = item['fields']
        bot_token = fields.get('bot_token')
        if bot_token and not model.objects.filter(bot_token=bot_token).exists():
            model.objects.create(**fields)


def add_data_to_type_db(data, model):
    for item in data:
        fields = item['fields']
        type = fields.get('type')
        if type and not model.objects.filter(type=type).exists():
            model.objects.create(**fields)


def add_data_to_client_db(data, model):
    for item in data:
        fields = item['fields']
        phone = fields.get('phone')
        if phone and not model.objects.filter(phone=phone).exists():
            model.objects.create(**fields)


def channel_id_finder(channel_data, id):
    for item in channel_data:
        if item['pk'] == id:
            return item['fields']['channel_id']


def type_id_finder(channel_type_data, id):
    for item in channel_type_data:
        if item['pk'] == id:
            return item['fields']['type']

def bot_id_finder(bot_data, id):
    for item in bot_data:
        if item['pk'] == id:
            return item['fields']['bot_token']


def add_data_to_keyword_db(data, model):
    for item in data:
        fields = item['fields']
        channel = fields.get('channel')
        text = fields.get('text')

        channel_id = channel_id_finder(json_loader("channels.json"), channel)
        channel_obj = Channels.objects.get(channel_id=channel_id)
        if not model.objects.filter(text=text, channel=channel_obj).exists():
            model.objects.create(
                text=text,
                channel=channel_obj
            )


def add_data_to_channel_db(data, model):
    print(100 * "*")
    for item in data:
        pk = item['pk']
        channel_name = item['fields'].get('channel_name')
        my_channel = item['fields'].get('my_channel')
        print("my_channel", pk, my_channel)
        bot = item['fields'].get('bot')
        type = item['fields'].get('type')
        channel_link = item['fields'].get('channel_link')
        channel_id = item['fields'].get('channel_id')
        type_by_id = type_id_finder(json_loader("channel_type.json"), type)
        print("type_by_id", type_by_id)
        type_obj = Channel_type.objects.get(type=type_by_id)
        print("type_obj", type_obj)

        if not model.objects.filter(channel_id=channel_id).exists():
            if my_channel == False:
                print("my_channel", channel_id, my_channel)
                model.objects.create(
                    channel_name=channel_name,
                    channel_link=channel_link,
                    my_channel=my_channel,
                    channel_id=channel_id,
                    bot=bot,
                    type=type_obj)
            if my_channel == True:
                bot_token = bot_id_finder(json_loader("user_data.json"), bot)
                bot_obj = Bot.objects.get(bot_token=bot_token)
                print("my_channel", channel_id, my_channel)
                model.objects.create(
                    channel_name=channel_name,
                    channel_link=channel_link,
                    my_channel=my_channel,
                    channel_id=channel_id,
                    bot=bot_obj,
                    type=type_obj)


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            bot_data = json_loader("user_data.json")
            channel_type_data = json_loader("channel_type.json")
            client_data = json_loader("client.json")
            channels_data = json_loader("channels.json")
            keyword_data = json_loader("keyword.json")

            add_data_to_bot_db(bot_data, Bot)
            add_data_to_type_db(channel_type_data, Channel_type)
            add_data_to_client_db(client_data, Client_Settings)
            add_data_to_channel_db(channels_data, Channels)
            add_data_to_keyword_db(keyword_data, KeywordChannelAds)

            print("Data loaded successfully")
        except Exception as e:
            logger.exception("Error occurred while loading data")
            print("An error occurred while loading data. Please check logs for more details.")
