from django.db import models
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Profile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, height_field=256, width_field=256 )
    bio = models.TextField(null=True, blank=True)
    xp = models.IntegerField(default=0)
    pepitas = models.IntegerField(default=0)
    

