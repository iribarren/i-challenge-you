from django.db import models
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Challenge(models.Model):
    dummy = models.IntegerField(default=3)

    def __str__(self):
        return str(self.dummy)
