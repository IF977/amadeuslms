# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-03 19:10
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Created Date')),
            ],
            options={
                'verbose_name_plural': 'Actions',
                'verbose_name': 'Action',
            },
        ),
        migrations.CreateModel(
            name='Action_Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Action_Resources',
                'verbose_name': 'Action_Resource',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Date and Time of action')),
            ],
            options={
                'verbose_name_plural': 'Logs',
                'verbose_name': 'Log',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Message')),
                ('read', models.BooleanField(default=False, verbose_name='Read')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Date and Time of action')),
                ('action_resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Action_Resource', verbose_name='Action_Resource')),
            ],
            options={
                'verbose_name_plural': 'Notifications',
                'verbose_name': 'Notification',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True, verbose_name='Slug')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Created Date')),
                ('url', models.CharField(default='', max_length=100, verbose_name='URL')),
            ],
            options={
                'verbose_name_plural': 'Resources',
                'verbose_name': 'Resource',
            },
        ),
    ]
