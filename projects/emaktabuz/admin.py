from django.contrib import admin

from .models import LogSenderBot, UserData


# Register your models here.


@admin.register(LogSenderBot)
class LogSenderBotAdmin(admin.ModelAdmin):
    list_display = ("token", "channel_id",)


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ("login", "password", "last_login", "today_status")
    list_filter = ("last_login", "today_status")

