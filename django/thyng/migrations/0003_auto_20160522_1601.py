# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thyng', '0002_auto_20160522_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]