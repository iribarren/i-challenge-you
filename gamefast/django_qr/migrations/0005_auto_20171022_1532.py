# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-22 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_qr', '0004_auto_20171022_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='qr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_actions', to='django_qr.Qr'),
        ),
    ]
