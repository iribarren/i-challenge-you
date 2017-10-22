from django.contrib import admin
from .models import *

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('game', 'challenger', 'challenged')

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Game)
