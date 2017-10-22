from django.db import models

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from abc import ABC, abstractmethod, ABCMeta

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Qr(models.Model):
    reference = models.CharField(max_length=50)
    enabled = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now=True)


    class Meta:
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['enabled']),
        ]

class UserAction(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL)
    action = models.ForeignKey('Action')
    timestamp = models.DateTimeField(auto_now=True)


class Action(models.Model):
    ACTION_TYPE_ADD = 0
    ACTION_TYPE_REMOVE = 1
    ACTION_TYPE_SHOW = 2
    ACTION_TYPE_EDIT = 3

    ACTION_TYPE_CHOICES = (
        (ACTION_TYPE_ADD, _('Add')),
        (ACTION_TYPE_REMOVE, _('Remove')),
        (ACTION_TYPE_SHOW, _('Show')),
        (ACTION_TYPE_EDIT, _('Edit')),
    )

    qr = models.ForeignKey('Qr', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    action_type = models.PositiveSmallIntegerField(
        choices = ACTION_TYPE_CHOICES,
    )
    content_object_field = models.CharField(max_length=100,null=True,blank=True)
    content_object_field_value = models.CharField(max_length=100,null=True,blank=True)
    expiration_date = models.DateTimeField(null=True,blank=True)
    priority = models.PositiveSmallIntegerField(default=0)
    stop = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)
    max_global_uses = models.PositiveSmallIntegerField(default=0) #0 = infinite
    max_personal_uses = models.PositiveSmallIntegerField(default=0) #0 = infinite

"""
class Scaneable(metaclass=ABCMeta):
    @abstractmethod
    def add(self): pass

    @abstractmethod
    def show(self): pass

    @abstractmethod
    def remove(self): pass

    @abstractmethod
    def edit(self, model_field, value): pass
"""
