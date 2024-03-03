from django.db import models

from central_system.utils.bot import get_info


# Create your models here.


class LogSenderBot(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=255, unique=True)
    bot_username = models.CharField(max_length=125, blank=True, null=True)
    channel_name = models.CharField(max_length=255, null=True, blank=True)
    channel_id = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra_field = models.JSONField(null=True, blank=True)
    def save(self, *args, **kwargs):
        username, name = get_info(bot_token=self.token)

        self.bot_username = username
        self.name = name
        if not self.channel_id.startswith('-'):
            if self.channel_id.startswith('100'):
                self.channel_id = '-' + self.channel_id
            else:
                self.channel_id = '-100' + self.channel_id

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "LogBot"
        verbose_name_plural = "LogBot"
class BackupDbBot(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=255, unique=True)
    bot_username = models.CharField(max_length=125, blank=True, null=True)
    channel_name = models.CharField(max_length=255, null=True, blank=True)
    channel_id = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra_field = models.JSONField(null=True, blank=True)
    def save(self, *args, **kwargs):
        username, name = get_info(bot_token=self.token)

        self.bot_username = username
        self.name = name
        if not self.channel_id.startswith('-'):
            if self.channel_id.startswith('100'):
                self.channel_id = '-' + self.channel_id
            else:
                self.channel_id = '-100' + self.channel_id

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "BackupDb"
        verbose_name_plural = "BackupDb"
