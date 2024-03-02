import datetime
import logging

import requests
# from googletrans import Translator
from telegram import Update
from telegram.ext import CallbackContext

from projects.chatgpt_bot.models import LogSenderBot
from .buttons.inline_keyboard import language_list, \
    language_list_keyboard, inline_lang_generator
from .buttons.keyboard import generate_keyboard
from .models import TelegramProfile
from .translate_integrations import translate_text_with_lang
from .utils.decarators import get_member

logger = logging.getLogger(__name__)

from asgiref.sync import sync_to_async

from .models import TranslatorConversation


@sync_to_async
def set_lang(translator_user, lang, native: bool):
    print(100 * '$')
    print(translator_user, lang, native)
    print(translator_user.native_language, translator_user.target_language)
    if translator_user:
        print("Translator User exists")
        if native:
            print("Native Language")
            translator_user.native_language = lang
            translator_user.save()
            print(translator_user.native_language, translator_user.target_language)
            return True
        if not native:
            translator_user.target_language = lang
            translator_user.save()

            return True
    else:
        return None


@sync_to_async
def save_conversation(user, text, translated_text, source_lang, target_lang):
    TranslatorConversation.objects.create(
        user=user,
        text=text,
        translated_text=translated_text,
        source_language=source_lang,
        target_language=target_lang
    )


def send_to_telegram(bot_token, chat_id, filename, caption):
    caption += f"\nDate: {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    files = {'document': open(f"{filename}", 'rb')}
    data = {'chat_id': chat_id, 'caption': caption} if caption else {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    return response.json()


@sync_to_async()
def send_msg_log(message):
    # Define maximum length for each message chunk
    max_length = 4096

    if LogSenderBot.objects.all().count() > 0:
        token = LogSenderBot.objects.last().token
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


@get_member
async def start(update: Update, context: CallbackContext, *args, **kwargs):
    if update.callback_query:
        await update.callback_query.edit_message_text(
            "Welcome to the translator bot. Please select your native language.",
            reply_markup=language_list_keyboard("native"))
    else:
        await update.message.reply_text("Welcome to the translator bot. Please select your native language.",
                                        reply_markup=language_list_keyboard("native"))


@get_member
async def about(update: Update, context: CallbackContext, *args, **kwargs):
    print("start", update.effective_user.username)
    """Send a message asynchronously when the command /start is issued."""
    message = "if you have some questions or questions about bot creation you can contact the creator via the link below => " + '<a href="https://t.me/+998939708050">ADMIN</a>'
    try:
        await update.message.reply_html(message)
    except Exception as e:
        logger.error(f"Error in start command: {e}")


@get_member
async def change_native_lang(update: Update, context: CallbackContext, translator_user: TelegramProfile, *args,
                             **kwargs):
    if update.callback_query:
        await update.callback_query.edit_message_text(
            "Please select your native language.",
            reply_markup=language_list_keyboard("target"))
    else:
        await update.message.reply_text("Welcome to the translator bot. Please select your native language.",
                                        reply_markup=language_list_keyboard("target"))


@get_member
async def settings_user(update: Update, context: CallbackContext, translator_user: TelegramProfile, *args, **kwargs):
    native_lang, target_lang = translator_user.native_language, translator_user.target_language
    native_lang_name = next((item["name"] for item in language_list if item["id"] == native_lang), None)
    target_lang_name = next((item["name"] for item in language_list if item["id"] == target_lang), None)
    print(update)

    if update.message and update.message.entities and update.message.entities[0].type == "bot_command":
        if update.callback_query:
            await update.callback_query.edit_message_text(
                f"Your  language is {native_lang_name} => {target_lang_name}",
                reply_markup=inline_lang_generator(native_lang, target_lang))
        else:
            await update.message.reply_text(
                f"Your  language is {native_lang_name} => {target_lang_name}",
                reply_markup=inline_lang_generator(native_lang, target_lang))
    if update.callback_query:
        query = update.callback_query
        query_data = update.callback_query.data
        if query_data.startswith("change_lang_"):
            type_lang = query_data.split("_")[-1]
            if type_lang == "native":
                await query.edit_message_text(
                    f"Can you select your native language?",
                    reply_markup=language_list_keyboard("reset_native"))
            if type_lang == "target":
                await query.edit_message_text(
                    f"Can you select your target language?",
                    reply_markup=language_list_keyboard("reset_target"))
        if query_data.startswith("language_reset_native"):
            lang = query.data.split("language_reset_native_")[1]
            await set_lang(translator_user, lang, True)
            native_lang, target_lang = translator_user.native_language, translator_user.target_language
            native_lang_name = next((item["name"] for item in language_list if item["id"] == native_lang), None)
            target_lang_name = next((item["name"] for item in language_list if item["id"] == target_lang), None)
            await update.callback_query.edit_message_text(
                f"Your  language is {native_lang_name} => {target_lang_name}",
                reply_markup=inline_lang_generator(native_lang, target_lang))

        if query_data.startswith("language_reset_target"):
            lang = query.data.split("language_reset_target_")[1]
            await set_lang(translator_user, lang, False)
            native_lang, target_lang = translator_user.native_language, translator_user.target_language
            native_lang_name = next((item["name"] for item in language_list if item["id"] == native_lang), None)
            target_lang_name = next((item["name"] for item in language_list if item["id"] == target_lang), None)
            await update.callback_query.edit_message_text(
                f"Your  language is {native_lang_name} => {target_lang_name}",
                reply_markup=inline_lang_generator(native_lang, target_lang))
    else:
        await update.message.reply_text(
            f"Your  language is {native_lang_name} => {target_lang_name}",
            reply_markup=inline_lang_generator(native_lang, target_lang))


@get_member
async def set_native_lang(update: Update, context: CallbackContext, translator_user: TelegramProfile, *args, **kwargs):
    print("set_native_lang")
    print(translator_user)
    print(update.callback_query.data.split("_")[-1])
    query = update.callback_query
    lang = query.data.split("_")[-1]
    lang_name = next((item["name"] for item in language_list if item["id"] == lang), None)
    await set_lang(translator_user, lang, True)
    if lang_name:
        await query.edit_message_text(
            "Native language has been set to " + lang_name + "\nPlease select your target language",
            reply_markup=language_list_keyboard("target"))
        await query.answer("Language has been set to " + lang_name)
    else:
        await query.message.reply_text("Language not found.")
        await query.answer("Language not found.")


@get_member
async def set_target_lang(update: Update, context: CallbackContext, translator_user: TelegramProfile, *args, **kwargs):
    query = update.callback_query
    lang = query.data.split("_")[-1]
    lang_name = next((item["name"] for item in language_list if item["id"] == lang), None)
    await set_lang(translator_user, lang, False)

    if lang_name:
        await query.edit_message_text(f"Target language has been set to {lang_name} , please send word or sentece!")
        await query.answer("Language has been set to " + lang_name)
    else:
        await query.message.reply_text("Language not found.")
        await query.answer("Language not found.")


@get_member
async def translator(update: Update, context: CallbackContext, translator_user: TelegramProfile, *args, **kwargs):
    msg = update.message.text
    native_lang, target_lang = translator_user.native_language, translator_user.target_language
    word = await translate_text_with_lang(msg, native_lang, target_lang)
    await save_conversation(translator_user, msg, word.translated_text, native_lang, target_lang)
    buttons = ["Change Language", "History conversation", "About", "Restart"]
    reply_markup = generate_keyboard(buttons)
    await update.message.reply_text(word.translated_text, reply_markup=reply_markup)
