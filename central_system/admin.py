from django.contrib import admin

from central_system.models import LogSenderBot


# Register your models here.

@admin.register(LogSenderBot)
class LogSenderBotAdmin(admin.ModelAdmin):
    list_display = ("id", "token", "channel_id",)
