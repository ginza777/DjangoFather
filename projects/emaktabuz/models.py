from django.db import models


class UserData(models.Model):
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    today_status = models.BooleanField(default=False)

    def __str__(self):
        return self.login
