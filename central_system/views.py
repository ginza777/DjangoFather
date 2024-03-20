import datetime

import requests
from asgiref.sync import sync_to_async
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from central_system.models import LogSenderBot
from central_system.serializers import ChannelsSerializer, ClientSettingsSerializer, BotSerializer, \
    ChannelTypeSerializer, KeywordChannelAdsSerializer
from projects.telegram_post_scrapper.models import Client_Settings, Bot, Channel_type, Channels, KeywordChannelAds


class ChannelsApi(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Channels.objects.all()
    serializer_class = ChannelsSerializer


class ClientSettingsApi(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Client_Settings.objects.all()
    serializer_class = ClientSettingsSerializer


class BotApi(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Bot.objects.all()
    serializer_class = BotSerializer


class ChannelTypeApi(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Channel_type.objects.all()
    serializer_class = ChannelTypeSerializer


class KeywordChannelAdsApi(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = KeywordChannelAds.objects.all()
    serializer_class = KeywordChannelAdsSerializer


def send_to_telegram(bot_token, chat_id, filename, caption):
    caption += f"\nDate: {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    files = {'document': open(f"{filename}", 'rb')}
    data = {'chat_id': chat_id, 'caption': caption} if caption else {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    return response.json()


def send_msg_log(message):
    # Define maximum length for each message chunk
    max_length = 4096
    token, chat_id = None, None
    if LogSenderBot.objects.all().count() > 0:
        token = LogSenderBot.objects.last().token
        chat_id = LogSenderBot.objects.last().channel_id
    else:
        token = "6567332198:AAHRaGT5xLJdsJbWkugqgSJHbPGi8Zr2_ZI"
        chat_id = -1002120483646

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
        print("r: ", r.status_code)
        print("r: ", r.text)
        if r.status_code != 200:
            return False

    return True


# -----------------Google Translate API-----------------#
from google.cloud import translate
import logging

logger = logging.getLogger(__name__)

PROJECT_ID = "ubuntu-407908"
assert PROJECT_ID
PARENT = f"projects/{PROJECT_ID}"


@sync_to_async
def translator(text: str, target_language_code: str, ) -> translate.Translation:
    try:
        client = translate.TranslationServiceClient()
        response = client.translate_text(
            parent=PARENT,
            contents=[text],
            target_language_code=target_language_code,
            mime_type="text/plain",

        )
        print(response.translations[0])
        return response.translations[0].translated_text
    except:
        return text
