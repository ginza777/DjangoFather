from django.contrib import admin

from .models import TelegramProfile, TelegramBot


@admin.register(TelegramProfile)
class TranslatorUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "native_language", "target_language")


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ("name", "bot_token")
