# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-12 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160908_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='link',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='URL'),
        ),
    ]
