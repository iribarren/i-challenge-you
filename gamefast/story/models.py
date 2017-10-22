from django.db import models
from django.utils.translation import ugettext_lazy as _

class Story(models.Model):
    TYPE_TXT = 0
    TYPE_LINK = 1
    TYPE_HTML = 2
    TYPE_IMG = 3

    TYPE_CHOICES = (
        (TYPE_TXT, _('Text')),
        (TYPE_LINK, _('Link')),
        (TYPE_HTML, _('HTML')),
        (TYPE_IMG, _('Image'))
    )
    name=models.CharField(max_length=30, null=True, blank=True)
    content_type=models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES,
        default=TYPE_TXT
    )
    data = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.name

    def add(self,user): pass
    def show(self,user):
        return (
            (name, self.name),
            (content_type, self.content_type),
            (data = self.data),)            
        )
    def remove(self,user): pass
    def edit(self, model_field, value): pass
