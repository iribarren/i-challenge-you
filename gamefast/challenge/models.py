from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Game(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def add(self):pass
    def edit(self):pass
    def remove(self):pass
    def show(self):
        return self.challenges

class Challenge(models.Model):
    STATE_LAUNCHED = 0
    STATE_ACCEPTED = 1
    STATE_REJECTED = 2
    STATE_FINISHED = 3

    STATE_CHOICES = (
        (STATE_LAUNCHED, _('Launched')),
        (STATE_ACCEPTED, _('Accepted')),
        (STATE_REJECTED, _('Rejected')),
        (STATE_FINISHED,_('Finished')),
    )

    challenger = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='challenges_launched',    
    ) 
    challenged = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='challenges_received'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    game = models.ForeignKey('Game',on_delete=models.PROTECT)
    state = models.PositiveSmallIntegerField(
        choices=STATE_CHOICES,
        default=STATE_LAUNCHED,
    )
    result = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return self.game
