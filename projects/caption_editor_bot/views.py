import logging
import time
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import CallbackContext
from .models import Keyword, Channel
from central_system.views import send_msg_log

logger = logging.getLogger(__name__)


async def cap_killer(update: Update, context: CallbackContext):
    time.sleep(2)
    """Send a message asynchronously when the command /start is issued."""
    if update.channel_post and update.channel_post.chat.type == "channel":
        print("this is channel message")
        chat_id = update.channel_post.chat.id
        message_id = update.channel_post.message_id
        caption = update.channel_post.caption or ''
        print("channel_post:",chat_id)
        # print(new_caption)
        try:
            status = await exist_checker(chat_id)
            print("status:", status)
            if status:
                new_caption = await filter_caption(caption, chat_id)
                await context.bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=new_caption)
            if not status:
                message = "caption killer bot\n"+"adminga qo'shilmagan" + f"""\n{update.channel_post.sender_chat.title}\n{update.channel_post.sender_chat.type}\n{update.channel_post.sender_chat.id}"""
                print(message)
                await sync_to_async(send_msg_log)(message)
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            message = "caption killer bot\n" + f"Error in start command: {e}"
            await sync_to_async(send_msg_log)(message)


@sync_to_async
def exist_checker(chat_id):
    if Channel.objects.filter(channel_id=chat_id).exists():
        return True
    else:
        return False


@sync_to_async
def filter_caption(caption: str, channel_id) -> str:
    print(channel_id)
    if Channel.objects.filter(channel_id=channel_id).exists():
        print("channel exist")
        channel = Channel.objects.get(channel_id=channel_id)
        keyword_texts = Keyword.objects.filter(channel=channel)
        keyword_text_list = [keyword.text for keyword in keyword_texts]
        print("channel:", channel)
        print(keyword_text_list)
        for key_word in keyword_text_list:
            caption = caption.replace(key_word, '')  # Fixed here, you need to assign the replaced caption back
        # caption = '\n'.join(line for line in caption.splitlines() if line.strip())
        caption += F"\n\n🐾꯭꯭꯭🇸꯭꯭ཽཾ𝐇꯭꯭꯭ི𝐞ྀ𝐢꯭꯭꯭ི𝐤꯭꯭꯭ྀ𝐡꯭꯭꯭꯭ི🐾꯭꯭\n\n{channel.channel_sign}"
        return caption
    return caption



async def start(update: Update, context: CallbackContext, *args, **kwargs):
    print("start", update.effective_user.username)
    """Send a message asynchronously when the command /start is issued."""
    message = "if you have some questions or questions about bot creation you can contact the creator via the link below => " + '<a href="https://t.me/+998939708050">ADMIN</a>'
    try:
        await update.message.reply_html(message)
    except Exception as e:
        logger.error(f"Error in start command: {e}")




async def about(update: Update, context: CallbackContext, *args, **kwargs):
    print("start", update.effective_user.username)
    """Send a message asynchronously when the command /start is issued."""
    message = "if you have some questions or questions about bot creation you can contact the creator via the link below => " + '<a href="https://t.me/+998939708050">ADMIN</a>'
    try:
        await update.message.reply_html(message)
    except Exception as e:
        logger.error(f"Error in start command: {e}")
