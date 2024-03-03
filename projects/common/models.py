from django.db import models
from .utils.bot import set_webhook_sync, get_info
import uuid

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


class TelegramProfile(models.Model):
    class Language(models.TextChoices):
        UZBEK = "uz", "Uzbek"
        ENGLISH = "en", "English"
        RUSSIAN = "ru", "Russian"
        SPANISH = "es", "Spanish"
        FRENCH = "fr", "French"
        GERMAN = "de", "German"

    bot = models.ManyToManyField(TelegramBot)
    telegram_id = models.PositiveBigIntegerField(unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, choices=Language.choices, default=Language.UZBEK, null=True)
    is_bot = models.BooleanField(default=False)
    user_token = models.UUIDField(unique=True, null=True, blank=True)
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.user_token:
            self.user_token = uuid.uuid4()
        super(TelegramProfile, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"


