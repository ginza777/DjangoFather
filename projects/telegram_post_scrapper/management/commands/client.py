import asyncio
from asyncio import Queue, create_task
from concurrent.futures import ThreadPoolExecutor

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from telethon import TelegramClient, events
from telethon.tl.types import Message, MessageMediaPhoto

from ...models import Client_Settings, Channels, SomeErrors, Message as MessageModel, Filename
from ...views import listening_channels_view, message_log_view, random_string

message_queue = Queue()
is_processing = False

# Bot va Client sozlamalari
env = Client_Settings.objects.last()
channels = list(Channels.objects.filter(my_channel=False).values_list('channel_link', flat=True))
print(channels)
# ===========[log start]================
listening_channels_view(list(channels))
print("count:", len(channels))
# ===========[log end]================

# ThreadPoolExecutor obyektini yaratish
executor = ThreadPoolExecutor(max_workers=5)


async def process_queue(client):
    global is_processing
    while not message_queue.empty():
        is_processing = True
        event = await message_queue.get()
        # print(event.message)
        if isinstance(event.message, Message) and hasattr(event.message, 'media'):
            print(f"new message")
            # Rasmlar  va Captionlar uchun
            if isinstance(event.message.media, MessageMediaPhoto):
                if event.message.grouped_id is not None:
                    if event.message.grouped_id and event.message is not None and event.message.raw_text != '':
                        await process_grouped_media_with_caption(event, client)

                    if event.message.grouped_id and event.message.raw_text == '':
                        await process_grouped_media_without_caption(event, client)

                if event.message.grouped_id is None:
                    if event.message.grouped_id is None and event.message is not None and event.message.raw_text != '':
                        await process_single_media_with_caption(event, client)
                message_queue.task_done()
        is_processing = False


async def main():
    client = TelegramClient(env.phone, env.api_id, env.api_hash)
    await client.start()

    @client.on(events.NewMessage(chats=channels))
    async def my_event_handler(event):
        if not is_processing:
            create_task(process_queue(client))
        await message_queue.put(event)

    await client.run_until_disconnected()


async def process_grouped_media_with_caption(event, client):
    photo = event.media.photo
    group_id = event.message.grouped_id
    channel_id = event.message.peer_id.channel_id
    caption = event.message.raw_text
    caption_file = f'media/{group_id}/{group_id}-{random_string(7)}.txt'
    photo_file = f'media/{group_id}/{group_id}-{random_string(7)}.jpeg'

    await client.download_media(photo, file=photo_file)
    await write_caption_to_file(caption_file, caption)
    await crate_message(message_id=group_id, channel_id=channel_id, single_photo=False, caption=caption_file,
                        photo_file=photo_file)


async def process_grouped_media_without_caption(event, client):
    photo = event.media.photo
    group_id = event.message.grouped_id
    channel_id = event.message.peer_id.channel_id
    file_path = f'media/{group_id}/{group_id}-{random_string(7)}.jpeg'
    await client.download_media(photo, file=file_path)
    await crate_message(message_id=group_id, channel_id=channel_id, single_photo=False, caption=None,
                        photo_file=file_path)


async def process_single_media_with_caption(event, client):
    photo = event.media.photo
    message_id = event.message.id
    channel_id = event.message.peer_id.channel_id
    caption = event.message.raw_text
    file_path = f'media/{message_id}/{message_id}-{random_string(7)}.jpeg'
    caption_file = f'media/{message_id}/{message_id}-{random_string(7)}.txt'
    await client.download_media(photo, file=file_path)
    await write_caption_to_file(caption_file, caption)
    await crate_message(message_id=message_id, channel_id=channel_id, single_photo=True, caption=caption_file,
                        photo_file=file_path)


@sync_to_async
def crate_message(message_id, channel_id=None, single_photo=False, photo_file=None, caption=None):
    message, created = MessageModel.objects.get_or_create(message_id=message_id)
    # ===========[log start]================
    message_log_view(message, "DEF CREATE_MESSAGE")
    message_log_view(message,
                     f"message_id={message_id} channel_id={channel_id} single_photo={single_photo} photo_file={photo_file} caption={caption}")
    # ===========[log end]================

    if channel_id is not None:

        try:
            # ===========[log start]================
            message_log_view(message, f"IF CHANNEL_ID : TRY: CHANNEL_ID={channel_id}")
            # ===========[log end]================

            channel = Channels.objects.get(channel_id=f"-100{channel_id}", my_channel=False)
            message.channel_from = channel
            message.save()

            # ===========[log start]================
            message_log_view(message, f"channel_from={channel}  mavjud")
            # ===========[log end]================


        except Exception as e:
            # ===========[log start]================
            message_log_view(message, f"channel_from  mavjud emas sabab: {e}")
            # ===========[log end]================

    if photo_file is not None:

        try:
            # ===========[log start]================
            message_log_view(message, f"IF PHOTO_FILE : TRY: PHOTO_FILE={photo_file}")
            # ===========[log end]================

            file = Filename.objects.create(filename=photo_file, message_id=message_id, is_photo=True)
            file.save()
            message.photo = True
            message.photo_count = message.photo_count + 1
            message.save()

            # ===========[log start]================
            message_log_view(message, f"IF PHOTO_FILE : TRY: PHOTO_FILE={photo_file}  saqlandi")
            # ===========[log end]================
        except Exception as e:
            # ===========[log start]================
            message_log_view(message, f"IF PHOTO_FILE : EXCEPT: PHOTO_FILE={photo_file} saqlanmadi sabab: {e}")
            # ===========[log end]================

    if caption is not None:
        try:
            # ===========[log start]================
            message_log_view(message, f"CAPTION is not None : TRY: CAPTION={caption}")
            # ===========[log end]================
            file = Filename.objects.create(filename=caption, message_id=message_id, is_caption=True)
            message.caption = True
            file.save()
            message.save()
            # ===========[log start]================
            message_log_view(message, f"CAPTION : TRY: CAPTION={caption}  saqlandi")
            # ===========[log end]================
        except Exception as e:
            # ===========[log start]================
            message_log_view(message, f"IF CAPTION : EXCEPT: CAPTION={caption} saqlanmadi sabab: {e}")
            # ===========[log end]================

    if single_photo:
        try:
            message.single_photo = True
            message.photo_count = 1
            message.photo = True
            message.save()
            # ===========[log start]================
            message_log_view(message, f"IF SINGLE_PHOTO : TRY: SINGLE_PHOTO={single_photo}  saqlandi")
            # ===========[log end]================

        except Exception as e:
            # ===========[log start]================
            message_log_view(message, f"IF SINGLE_PHOTO : EXCEPT: SINGLE_PHOTO={single_photo} saqlanmadi sabab: {e}")
            # ===========[log end]================


async def write_caption_to_file(file_path, caption_text):
    try:
        with open(file_path, 'w') as f:
            f.write(caption_text)
        return True
    except:
        try:
            with open(file_path, 'w') as f:
                f.write(caption_text)
        except Exception as e:
            SomeErrors.objects.create(title="write_caption_to_file", error=e)


class Command(BaseCommand):
    help = 'Starts the Telegram listener'

    def handle(self, *args, **options):
        asyncio.run(main())
