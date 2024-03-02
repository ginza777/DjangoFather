from .models import Keyword, Channel, TelegramBot
from django.contrib import admin


class KeywordInline(admin.TabularInline):
    model = Keyword
    extra = 2


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'channel')


@admin.register(Channel)
class ChannelsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'channel_id')
    inlines = [KeywordInline]


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ("name", "bot_token")
