from django.contrib import admin

from .models import  UserData, ChannelLog


# Register your models here.



@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ("login", "password", "last_login", "today_status")
    list_filter = ("last_login", "today_status")

@admin.register(ChannelLog)
class ChannelLogAdmin(admin.ModelAdmin):
    list_display = ("channel_name", "channel_id", "bot_token", "created_at")
    list_filter = ("created_at",)