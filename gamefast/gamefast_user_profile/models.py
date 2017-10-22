from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Profile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, height_field=256, width_field=256 )
    bio = models.TextField(null=True, blank=True)
    xp = models.IntegerField(default=0)
    pepitas = models.IntegerField(default=0)

    def edit(self, model_field, value):
       old_value = getattr(self, model_field)
       if value.startswith("+"):
           new_value = old_value + int(value[1:])
       elif value.startswith("-"):
           new_value = old_value - int(value[1:])
       elif value.startswith("*"):
           new_value = old_value * int(value[1:])
       else:
           new_value = old_value

       setattr(self, model_field, new_value)
       self.save()

    def __str__(self):
        return u'{0} (xp:{1} / pepitas:{2})'.format(self.user,self.xp,self.pepitas)

    def add(self): pass

    def show(self):
        return self

    def remove(self): pass

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
