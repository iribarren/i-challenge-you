# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-21 17:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('action_type', models.PositiveSmallIntegerField(choices=[(0, 'Add'), (1, 'Remove'), (2, 'Show'), (3, 'Edit')])),
                ('content_object_field', models.CharField(max_length=100)),
                ('content_object_field_value', models.CharField(max_length=100)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Qr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_number_uses', models.PositiveIntegerField(default=0)),
                ('max_number_uses_per_user', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='qr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_qr.Qr'),
        ),
    ]