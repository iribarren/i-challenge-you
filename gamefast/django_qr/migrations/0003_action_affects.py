# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-21 17:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_qr', '0002_auto_20171021_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='affects',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
