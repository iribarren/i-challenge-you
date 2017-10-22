from django.db import models

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from abc import ABC, abstractmethod, ABCMeta

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Qr(models.Model):
    reference = models.CharField(max_length=50)
    enabled = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now=True)

    def run_actions(self, user):
        if self.enabled == True:
            assigned_actions = self.assigned_actions.all() #TODO Maybe filter here?
            Action.run_action(assigned_actions,self, user)

    def __str__(self):
        return self.reference


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

    qr = models.ForeignKey('Qr', on_delete=models.CASCADE, related_name = 'assigned_actions')
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

    def get_instance(self):
        from django.contrib.contenttypes.models import ContentType

        ct_class = self.content_type.model_class()
        ct_instance = ct_class.objects.get(pk=self.object_id)
        return ct_instance

    @staticmethod
    def run_actions(action_list, qr, user):
        now = timezone.now()
        results = []
        ordered_action_list = action_list.filter(enabled=True).order_by('-priority')
        for action in ordered_action_list:
            if (action.expiration_date > now or action.expiration_date == None):
                #Check max_global_uses
                nb_global_uses = UserAction.objects.filter(action=action).count()
                if nb_global_uses >= action.max_global_uses:
                    results.append({'action_id': action.pk, 'result': 'Maximum global usages exceeded'})
                    continue #Next rule!!
                #Check max_personal_uses
                nb_max_personal_uses = UserAction.objects.filter(action=action,user=user).count()
                if nb_max_personal_uses >= action.max_personal_uses:
                    results.append({'action_id': action.pk, 'result': 'Maximum personal usages exceeded'})
                    continue #Next rule!!

                #Instantiate the remote object
                ct_instance = action.get_instance()
                
                #Switch action
                if action.action_type == ACTION_TYPE_ADD:
                    results.append({'action_id': action.pk, 'result': ct_instance.add(user)})
                elif action.action_type == ACTION_TYPE_REMOVE:
                    results.append({'action_id': action.pk, 'result': ct_instance.remove(user)})
                elif action.action_type == ACTION_TYPE_SHOW:
                    results.append({'action_id': action.pk, 'result': ct_instance.show(user)})
                elif action.action_type == ACTION_TYPE_EDIT:
                    results.append({'action_id': action.pk, 'result': ct_instance.edit(action.content_object_field, action.content_object_field_value)})
                else:
                    results.append({'action_id': action.pk, 'result': "Unsupported action"})

                #Break if stop
                if action.stop == True:
                    break
        return results
        

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
