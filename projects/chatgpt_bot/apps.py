import asyncio
import traceback

import django.core.exceptions
import environ
import requests.exceptions
import telegram
from asgiref.sync import sync_to_async
from django.apps import AppConfig
from django.db import connection
from django.db.utils import ProgrammingError

from .utils.bot import set_webhook

env = environ.Env()
environ.Env.read_env()

@sync_to_async
def create_superuser():
    if "auth_user" in connection.introspection.table_names():
        username = env.str("SUPERUSER_USERNAME") or "sherzamon"
        email = env.str("SUPERUSER_EMAIL") or "sherzamon@gmail.com"
        password = env.str("SUPERUSER_PASSWORD") or "sherzAmon20001A"
        try:
            from django.contrib.auth.models import User

            # Check if the user already exists
            if not User.objects.filter(username=username).exists():
                # Create a new superuser
                User.objects.create_superuser(username, email, password)
                print(f"Superuser '{username}' created successfully.")
            else:
                print(f"Superuser '{username}' already exists.")
        except ProgrammingError:
            print("you must migrate")


class ChatgptBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "projects.chatgpt_bot"

    def ready(self):
        # call_command('migrate', interactive=False)
        asyncio.run(create_superuser())
        asyncio.run(self.setup_webhook())

    async def setup_webhook(self):
        print("setup_webhook...")
        try:
            bot_tokens = await self.get_bot_tokens()
            print("bot_tokens: ", bot_tokens)
            for bot_token in bot_tokens:
                await set_webhook(bot_token)
        except telegram.error.RetryAfter:
            pass
        except requests.exceptions.ConnectionError:
            print("Connection error. Please check your internet connection.")
        except django.core.exceptions.ImproperlyConfigured:
            print("Improperly configured. Please check your settings.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()

    @sync_to_async
    def get_bot_tokens(self):
        try:
            from .models import TelegramBot
            bot_tokens = list(TelegramBot.objects.all().values_list("bot_token", flat=True))
        except ProgrammingError:
            bot_tokens = []

        return bot_tokens