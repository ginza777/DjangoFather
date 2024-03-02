from .models import TelegramProfile, TranslatorConversation,TelegramBot
from django.contrib import admin


@admin.register(TelegramProfile)
class TranslatorUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "native_language", "target_language")


@admin.register(TranslatorConversation)
class TranslatorAdmin(admin.ModelAdmin):
    list_display = ("user", "text", "translated_text", "source_language", "target_language", "created_at")
    list_filter = ("source_language", "target_language", "created_at")

@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ("name","bot_token")
