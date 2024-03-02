from django.db import models
from django.core.exceptions import ValidationError
from .utils.bot import set_webhook_sync, get_info


class TelegramBot(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    bot_token = models.CharField(max_length=255, unique=True)
    bot_username = models.CharField(max_length=125, blank=True, null=True)
    extra_field = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        set_webhook_sync(self.bot_token)
        username, name = get_info(bot_token=self.bot_token)
        self.bot_username = username
        self.name = name

        super(TelegramBot, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "TelegramBot"
        verbose_name_plural = "TelegramBot"


class Channel(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    channel_id = models.CharField(max_length=200, null=True, blank=True)
    channel_sign = models.TextField()

    def __str__(self):
        return self.name


class Keyword(models.Model):
    text = models.TextField()
    channel = models.ForeignKey(Channel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ('text', 'channel')
        # app_label = 'setting_ads'
