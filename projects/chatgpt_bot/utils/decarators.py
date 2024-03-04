from channels.db import database_sync_to_async
from django.utils.translation import activate

from projects.chatgpt_bot import models

def get_member(func):
    async def wrap(update, context, *args, **kwargs):
        user_id, first_name, last_name, username = 0, "", "", ""

        print(100 * "*-")
        try:
            if update.message.chat.type == "private":
                print("Private Chat")
                user_id = update.message.chat_id
                first_name = update.effective_user.first_name
                last_name = update.effective_user.last_name
                username = update.effective_user.username
            elif update.message.chat.type == "group" or update.message.chat.type == "supergroup":
                print("Group Chat,type=", update.message.chat.type)
                user_id = update.message.from_user.id
                first_name = update.message.from_user.first_name
                last_name = update.message.from_user.last_name
                username = update.message.from_user.username
            elif update.callback_query:
                print("Callback Query")
                user_id = update.callback_query.from_user.id
                first_name = update.callback_query.from_user.first_name
                last_name = update.callback_query.from_user.last_name
                username = update.callback_query.from_user.username

        except AttributeError:
            print("Attribute Error")
            user_id = update.callback_query.from_user.id
            first_name = update.callback_query.from_user.first_name
            last_name = update.callback_query.from_user.last_name
            username = update.callback_query.from_user.username


        print("User ID:", user_id)
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Username:", username)

        bot = await models.TelegramBot.objects.aget(bot_username=context.bot.username)
        current_model = await models.GptModels.objects.aget(model="gpt-3.5-turbo-16k")
        current_chat_mode = await models.Chat_mode.objects.aget(key="assistant")
        language_code = update.effective_user.language_code
        try:
            selected_language = models.Language(language_code)
        except ValueError:
            # Handle the case where the language code is not in Language choices
            selected_language = models.Language.UZBEK  # Set a default language or handle accordingly
            print(f"Language code '{language_code}' not found in choices. Using default language.")

        print(f"Selected Language: {selected_language}")

        # Convert synchronous database operations to asynchronous
        user, created = await get_or_create_user(user_id, first_name, last_name, username, selected_language, bot, current_model, current_chat_mode)

        return await func(update, context, user, *args, **kwargs)

    return wrap

# Define a coroutine function to create or retrieve user asynchronously
@database_sync_to_async
def get_or_create_user(user_id, first_name, last_name, username, selected_language, bot, current_model, current_chat_mode):
    user, created = models.TelegramProfile.objects.get_or_create(
        telegram_id=user_id,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "language": selected_language,
        },
    )
    if not created:
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.language = selected_language
        user.bot.add(bot)
        user.save()
    else:
        user.language = selected_language
        user.bot.add(bot)
        user.save()

    if user.current_chat_mode is None:
        user.current_chat_mode = current_chat_mode
        user.save()
    if user.current_model is None:
        user.current_model = current_model
        user.save()

    return user, created
