import uuid

from django.db import models

from .utils.bot import get_info, set_webhook_sync

AVAILABLE_TEXT_MODELS_CHOICES = [
    ("gpt-3.5-turbo", "GPT-3.5 Turbo"),
    ("gpt-3.5-turbo-16k", "GPT-3.5 Turbo 16k"),
    ("gpt-4-1106-preview", "GPT-4 1106 Preview"),
    ("gpt-4", "GPT-4"),
    ("text-davinci-003", "Text Davinci 003"),
]


class Language(models.TextChoices):
    UZBEK = "uz", "Uzbek"
    ENGLISH = "en", "English"
    RUSSIAN = "ru", "Russian"
    SPANISH = "es", "Spanish"
    FRENCH = "fr", "French"
    GERMAN = "de", "German"


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
    native_language = models.CharField(max_length=10, null=True, blank=True, default='no_lang')
    target_language = models.CharField(max_length=10, null=True, blank=True, default='no_lang')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.user_token:
            self.user_token = uuid.uuid4()
        super(TelegramProfile, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"


class TranslatorConversation(models.Model):
    user = models.ForeignKey(TelegramProfile, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    translated_text = models.TextField()
    source_language = models.CharField(max_length=10, null=True, blank=True)
    target_language = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
