from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Inventory(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return u'{0}\'s inventory'.format(self.user)

class Item (models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(null=True, blank=True, height_field=256, width_field=256)
    stored_in = models.ManyToManyField(
        Inventory,
        null = True,
        blank = True,
        related_name = 'items'
    )

    def __str__(self):
        return self.name;

    def add(self, user):
        user.inventory.items.add(self)
        user.inventory.save()
    def remove(self):
        user.inventory.items.delete(self)
        user.inventory.save()
    def edit(self): pass
    def show(self):
        return self;


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_inventory(sender, instance=None, created=False, **kwargs):
    if created:
        Inventory.objects.create(user=instance)
