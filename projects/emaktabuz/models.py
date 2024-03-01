from django.db import models


# Create your models here.

class LogSenderBot(models.Model):
    token = models.CharField(max_length=200, unique=True)
    channel_id = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.channel_id.startswith('-'):
            if self.channel_id.startswith('100'):
                self.channel_id = '-' + self.channel_id
            else:
                self.channel_id = '-100' + self.channel_id

        super().save(*args, **kwargs)


class UserData(models.Model):
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    today_status = models.BooleanField(default=False)

    def __str__(self):
        return self.login

# Create your models here.
