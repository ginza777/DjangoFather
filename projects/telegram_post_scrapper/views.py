import datetime
import json
import os
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from django.utils import timezone

from projects.telegram_post_scrapper.models import Listening_channels, Message_log, SomeErrors, Message_history, \
    Channels, Bot as LogSenderBot, \
    Filename, Message, KeywordChannelAds


# Create your views here.


def listening_channels_view(channel_list: list):
    for channel_link in channel_list:
        if Channels.objects.filter(channel_link=channel_link).exists():
            channel = Channels.objects.get(channel_link=channel_link)
            try:
                Listening_channels.objects.get(listening_channel=channel)
            except:
                try:
                    Listening_channels.objects.create(listening_channel=channel)
                except Exception as e:
                    SomeErrors.objects.create(title='listening_channels', error=e)
        else:
            SomeErrors.objects.create(title='listening_channels', error=f"{channel_link} not found")


def message_log_view(message, log, is_sent=False):
    try:
        message_log_instance = Message_log.objects.get(message=message)
        message_log_instance.log += '\n' + 100 * '-' + f"\n{log}"
        if is_sent is not None:
            message_log_instance.is_sent = is_sent
        message_log_instance.save()
    except Message_log.DoesNotExist:
        Message_log.objects.create(message=message, log=log, is_sent=is_sent)


def message_sent_status(message=None, status=False, channel_from=None, channel_to=None, type=None):
    try:
        message = Message_history.objects.get(message=message, from_channel=channel_from, to_channel=channel_to,
                                              type=type)
        message.sent_status = status
        message.time = timezone.now()
        message.save()
    except:
        Message_history.objects.create(message=message, sent_status=status, from_channel=channel_from,
                                       to_channel=channel_to, type=type)


def send_to_telegram(bot_token, chat_id, filename):
    caption = f"Ads_manager Date: {timezone.now()}"
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    files = {'document': open(f"{filename}", 'rb')}
    data = {'chat_id': chat_id, 'caption': caption} if caption else {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    return response.json()


def send_msg_log(message):
    # Define maximum length for each message chunk
    max_length = 4096

    if LogSenderBot.objects.all().count() > 0:
        token = LogSenderBot.objects.last().bot_token

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
        print("send_msg_log: r: ", r.status_code)
        print("send_msg_log: r: ", r.text)
        if r.status_code != 200:
            return False

    return True


def send_msg_simple(message, token, channel_id):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    params = {
        'chat_id': channel_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    r = requests.post(url, data=params)
    if r.status_code == 200:
        return True
    else:
        return False


def send_as_photo(image_caption, image, token, channel_id):
    url = f'https://api.telegram.org/bot{token}/sendPhoto'
    params = {
        'chat_id': channel_id,
        'caption': image_caption,
        'parse_mode': 'HTML',
        'photo': image,
    }
    r = requests.post(url, data=params)
    if r.status_code != 200:
        return False, r.status_code
    else:
        return True, r.status_code


def random_string(length):
    characters = string.ascii_letters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def check_caption_file_exist(message_id):
    file_path = Filename.objects.get(message_id=message_id, is_caption=True).filename
    if os.path.exists(file_path):
        return True
    return False


def filter_caption(message_id: str, channel_to_id: str):
    message = Message.objects.get(message_id=message_id)

    if Message.objects.get(message_id=message_id).caption:
        if check_caption_file_exist(message_id=message_id):
            caption_file_path = Filename.objects.get(message_id=message.message_id, is_caption=True).filename

            channel_from = Message.objects.get(message_id=message_id).channel_from
            channel_to = Channels.objects.get(channel_id=channel_to_id)

            keyword_texts = KeywordChannelAds.objects.filter(channel=channel_from)
            keyword_text_list = [keyword.text for keyword in keyword_texts]

            my_channel_text = KeywordChannelAds.objects.get(channel=channel_to).text

            with open(caption_file_path, 'r') as f:
                caption = f.read()
                caption = '\n'.join(line for line in caption.splitlines() if line.strip())
                for key_word in keyword_text_list:
                    caption = caption.replace(key_word, '')
                caption = caption + '\n' + my_channel_text
            return caption
        else:
            caption_file_path = Filename.objects.get(message_id=message.message_id, is_caption=True).filename
            with open(caption_file_path, 'r') as f:
                caption = f.read()
                caption = '\n'.join(line for line in caption.splitlines() if line.strip())
            return caption
    return None


def get_photo_filenames_by_message_id(message_id):
    messages = Filename.objects.filter(message_id=message_id, is_photo=True)
    photo_filenames = [message.filename for message in messages]
    return photo_filenames


def get_media_files_json_data(message_id):
    media_files = get_photo_filenames_by_message_id(message_id)
    media, files = [], {}
    for media_file in media_files:
        if media_file is not None:
            random_name = os.path.basename(media_file)
            media.append(
                {
                    'type': 'photo',
                    'media': f"attach://{random_name}",
                }
            )
            # Faylni byte ma'lumotga o'qish
            with open(media_file, 'rb') as f:
                file_data = f.read()
            files[random_name] = file_data

    from_channel = Message.objects.get(message_id=message_id).channel_from
    from_channel_type = from_channel.type
    my_channels_id_list = Channels.objects.filter(type=from_channel_type, my_channel=True).values_list(
        'channel_id', flat=True)

    data_list = []
    for ch_id in my_channels_id_list:
        caption = filter_caption(message_id, ch_id)
        media[0]['caption'] = f"#{message_id}\n" + caption
        media[0]['parse_mode'] = 'HTML'
        if caption is not None:
            Message_history.objects.create(
                message=Message.objects.get(message_id=message_id),
                from_channel=from_channel,
                to_channel=Channels.objects.get(channel_id=ch_id),
                type=from_channel_type,
                sent_status=False
            ).save()
            data_list.append(
                {
                    'data': {'chat_id': ch_id, 'media': json.dumps(media)},
                    'files': files,
                    'token': Channels.objects.get(channel_id=ch_id).bot.bot_token,
                    'channel_from': from_channel.channel_id,
                    'message_id': message_id,
                    'disable_notification': True
                }
            )

    return data_list


async def write_caption(file_path, caption_text):
    try:
        with open(file_path, 'w') as f:
            f.write(caption_text)
        return True
    except:
        return False


def send_msg(data):
    message = Message.objects.get(message_id=data['message_id'])
    url = f"https://api.telegram.org/bot{data['token']}/sendMediaGroup"
    # Fayllarni to'g'ri ko'rsatish uchun
    files = {key: (f"file{index}", file, 'application/octet-stream') for index, (key, file) in
             enumerate(data['files'].items())}

    data['data']['disable_notification'] = True
    r = requests.post(url, data=data['data'], files=files, )
    current_time = datetime.datetime.fromtimestamp(time.time())

    channel_from = Channels.objects.get(channel_id=data['channel_from'])
    channel_to = Channels.objects.get(channel_id=data['data']['chat_id'])
    type = channel_from.type

    if r.status_code == 200:
        message_sent_status(message=message, status=True, channel_from=channel_from, channel_to=channel_to, type=type)

        print(
            f"200 - {data['channel_from']} dan  {data['data']['chat_id']} ga  {data['message_id']} xabar yuborildi  yuborildi time: {current_time}"
        )
        message_log_view(message,
                         f"200 - {data['channel_from']} dan  {data['data']['chat_id']} ga  {data['message_id']} xabar yuborildi  yuborildi time: {current_time}",
                         is_sent=True)
        message.send_status = True
        message.save()





    if r.status_code == 400:
        message_sent_status(message=message, status=False, channel_from=channel_from, channel_to=channel_to, type=type)
        print(
            f"400 - {data['channel_from']} dan  {data['data']['chat_id']} ga  {data['message_id']} xabar yuborilmadi   error: {r.json()} time: {current_time}")
        message_log_view(message,
                         f"400 - {data['channel_from']} dan  {data['data']['chat_id']} ga  {data['message_id']} xabar yuborilmadi   error: {r.json()} time: {current_time}")


def send_messages(message_id):
    time.sleep(2)
    data_list = get_media_files_json_data(message_id)
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(send_msg, data_list)
        executor.shutdown(wait=True)
