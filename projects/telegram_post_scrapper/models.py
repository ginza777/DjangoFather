from django.core.exceptions import ValidationError
from django.db import models
import requests
def send_message_for_model(message, token, channel_id):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    params = {
        'chat_id': channel_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    r = requests.post(url, data=params)
    if r.status_code == 200:
        return True
    else:
        return False

class Client_Settings(models.Model):
    api_id = models.CharField(max_length=100, default='29441076')
    api_hash = models.CharField(max_length=100, default='2c170fe7bc8b8c8f8a1e1ad72db9710e')
    phone = models.CharField(max_length=100, default='+998993485501')
    token = models.CharField(max_length=100, null=True, blank=True)
    session = models.FileField(upload_to='session', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone

    class Meta:
        db_table = 'client_settings'
        # app_label = 'settings_ads_database'

    def save(self, *args, **kwargs):
        if self.session:
            self.session.name = str(self.phone) + '.session'
        super().save(*args, **kwargs)


class Bot(models.Model):
    bot_name = models.CharField(max_length=100)
    bot_token = models.CharField(max_length=100, unique=True)
    bot_link = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bot_name

    class Meta:
        db_table = 'bot_settings'
        # app_label = 'settings_ads_database'


class Channel_type(models.Model):
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type


class Channel_post_setting(models.Model):
    # new
    video = models.BooleanField(default=False)
    video_caption = models.BooleanField(default=False)
    photo = models.BooleanField(default=False)
    photo_caption = models.BooleanField(default=False)
    caption = models.BooleanField(default=False)
    text = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # class Meta:
    #     app_label = 'setting_ads'


class Channels(models.Model):
    channel_name = models.CharField(max_length=250)
    channel_link = models.CharField(max_length=250)
    channel_id = models.CharField(max_length=100, unique=True)
    my_channel = models.BooleanField(default=False)
    bot = models.ForeignKey(Bot, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey(Channel_type, on_delete=models.PROTECT)
    setting = models.OneToOneField(Channel_post_setting, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.channel_name

    class Meta:
        db_table = 'channels'
        unique_together = ('channel_id', 'my_channel')
        # app_label = 'setting_ads'

    def save(self, *args, **kwargs):
        if not self.channel_id.startswith('-'):
            if self.channel_id.startswith('100'):
                self.channel_id = '-' + self.channel_id
            else:
                self.channel_id = '-100' + self.channel_id
        if self.my_channel and self.bot is None:
            raise ValidationError('This channel is my channel, please select bot')
        if not self.my_channel:
            self.bot = None
        if self.my_channel and self.bot is not None:
            res = send_message_for_model('Hello', self.bot.bot_token, self.channel_id)
            if not res:
                raise ValidationError('This bot did not send message to this channel')
        if self.type is None:
            raise ValidationError('Please select channel type')

        if not self.channel_link.startswith('https://t.me/'):
            raise (ValidationError('Please enter valid channel link'))

        super().save(*args, **kwargs)

    def clean(self):
        if Channels.objects.filter(channel_id=self.channel_id).exclude(id=self.id).exists():
            raise ValidationError('This channel_id already exists')


class KeywordChannelAds(models.Model):
    text = models.TextField()
    channel = models.ForeignKey(Channels, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'keywordchannelads'
        unique_together = ('text', 'channel')
        # app_label = 'setting_ads'

    def clean(self):
        if self.channel.my_channel and KeywordChannelAds.objects.filter(channel=self.channel).exclude(
                id=self.id).exists():
            raise ValidationError('This channel already has keyword')


# Create your models here.
class Filename(models.Model):
    message_id = models.CharField(max_length=50)
    filename = models.CharField(max_length=100)
    is_caption = models.BooleanField(default=False)
    is_photo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename

    class Meta:
        db_table = 'filename'


class Message(models.Model):
    message_id = models.CharField(max_length=500, unique=True)
    caption = models.BooleanField(default=False)
    photo = models.BooleanField(default=False)
    channel_from = models.ForeignKey(Channels, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='from_channel_messages', limit_choices_to={'my_channel': False})
    delete_status = models.BooleanField(default=True)
    single_photo = models.BooleanField(default=False)
    send_status = models.BooleanField(default=False)
    photo_count = models.IntegerField(default=0)
    end = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.caption and self.photo:
            self.delete_status = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.message_id

    class Meta:
        db_table = 'message'


class Message_history(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    from_channel = models.ForeignKey(Channels, on_delete=models.CASCADE, related_name='from_channel', null=True,
                                     blank=True, limit_choices_to={'my_channel': False})
    to_channel = models.ForeignKey(Channels, on_delete=models.CASCADE, related_name='to_channel', null=True, blank=True,
                                   limit_choices_to={'my_channel': True})
    type = models.ForeignKey(Channel_type, on_delete=models.CASCADE, null=True, blank=True)
    sent_status = models.BooleanField(default=False)
    time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message.message_id

    class Meta:
        db_table = 'client_message_history'


class Message_log(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='message_log', null=True, blank=True)
    log = models.TextField()
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'message_log'
        verbose_name_plural = 'Message_log'


class Listening_channels(models.Model):
    listening_channel = models.OneToOneField(Channels, on_delete=models.CASCADE, related_name='listening_channel',
                                             null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'listening_channels'
        verbose_name_plural = 'listening_channels'

    def __str__(self):
        return f"{self.listening_channel}"


class Note(models.Model):
    title = models.CharField(max_length=255)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'note'
        verbose_name_plural = 'note'

    def __str__(self):
        return self.title


class SomeErrors(models.Model):
    title = models.CharField(max_length=255)
    error = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'some_errors'
        verbose_name_plural = 'some_errors'

    def __str__(self):
        return self.title
