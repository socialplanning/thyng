# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thyng', '0004_projectfeaturelet'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfeaturelet',
            name='title',
            field=models.CharField(default='Untitled Featurelet', max_length=50),
            preserve_default=False,
        ),
    ]
