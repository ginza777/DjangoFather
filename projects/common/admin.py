from django.contrib import admin

from .models import TelegramProfile, TelegramBot


@admin.register(TelegramProfile)
class TranslatorUserAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","username","language","telegram_id","user_token","is_bot",)


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ("name", "bot_token")
