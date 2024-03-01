from django.contrib import admin

from .models import Filename, Message, Message_history, Message_log, Listening_channels, Note, \
    SomeErrors, Client_Settings, Bot, Channels, KeywordChannelAds, Channel_type, Channel_post_setting


@admin.register(Filename)
class FilenameAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_id', 'filename', 'is_caption', 'is_photo', 'created_at', 'updated_at')
    search_fields = ('message_id', 'filename')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'message_id', 'caption', 'photo', 'channel_from_name', 'channel_to_count', 'delete_status', 'single_photo',
        'send_status',
        'photo_count', 'end', 'updated_at')

    def channel_from_name(self, obj):
        try:
            channel_name = obj.channel_from.channel_name
        except:
            channel_name = None
            SomeErrors.objects.create(title=f"Admin panelda channel_from_name error",
                                      error=f"channel_name={channel_name}\n message={obj.message_id} \n id={obj.id}")
        return channel_name

    def channel_to_count(self, obj):
        try:
            channel_to_count = Channels.objects.filter(type=obj.channel_from.type, my_channel=True).count()
        except:
            channel_to_count = None
            SomeErrors.objects.create(title=f"Admin panelda channel_to_count error",
                                      error=f"channel_to_count={channel_to_count}\n message={obj.message_id} \n id={obj.id}")
        return channel_to_count

    list_filter = ('delete_status', 'send_status', 'end', 'channel_from')
    # search filter
    search_fields = ('message_id',)


@admin.register(Message_history)
class Message_historyAdmin(admin.ModelAdmin):
    list_display = ('message', 'from_channel', 'to_channel', 'type', 'sent_status', 'time', 'created_at', 'updated_at')
    search_fields = ('message', 'from_channel', 'to_channel', 'type', 'sent_status', 'time')
    list_filter = ('from_channel', 'to_channel', 'type', 'sent_status', 'time')


@admin.register(Message_log)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ['message', 'is_sent', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['message__text']  # Assuming 'text' is a field in the Message model


@admin.register(Listening_channels)
class ListeningChannelsAdmin(admin.ModelAdmin):
    list_display = ['id', 'listening_channel', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['channel_id']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['title']


@admin.register(SomeErrors)
class SomeErrorsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['title']


# Register your models here.

admin.site.register(Client_Settings)


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('id', 'bot_name', 'bot_token', 'bot_link', 'created_at', 'updated_at')


# inline for channels vs KeywordChannelAds

class KeywordChannelAdsInline(admin.TabularInline):
    model = KeywordChannelAds
    extra = 2


@admin.register(Channel_post_setting)
class Channel_post_settingAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'video_caption', 'photo', 'photo_caption', 'caption', 'text')


@admin.register(Channels)
class ChannelsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'channel_name', 'channel_link', 'channel_id', 'my_channel', 'type', 'keyword_count', 'updated_at')
    inlines = [KeywordChannelAdsInline]
    list_filter = ['my_channel', 'type']

    def keyword_count(self, obj):
        return obj.keywordchannelads_set.count()


@admin.register(KeywordChannelAds)
class KeywordChannelAdsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'channel', 'created_at', 'updated_at')
    list_filter = ['channel__type']


admin.site.register(Channel_type)
