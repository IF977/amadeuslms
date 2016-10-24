# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-22 04:58
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True, verbose_name='Slug'),
        ),
    ]
