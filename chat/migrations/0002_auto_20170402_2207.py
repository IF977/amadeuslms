# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-03 01:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0014_auto_20170130_1828'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorytalk',
            name='conversation_ptr',
        ),
        migrations.RemoveField(
            model_name='categorytalk',
            name='space',
        ),
        migrations.RemoveField(
            model_name='generaltalk',
            name='conversation_ptr',
        ),
        migrations.RemoveField(
            model_name='subjecttalk',
            name='conversation_ptr',
        ),
        migrations.RemoveField(
            model_name='subjecttalk',
            name='space',
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='_my_subclass',
        ),
        migrations.AddField(
            model_name='talkmessages',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_subject', to='subjects.Subject', verbose_name='Subject'),
        ),
        migrations.AlterField(
            model_name='talkmessages',
            name='talk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_talk', to='chat.Conversation', verbose_name='Conversation'),
        ),
        migrations.AlterField(
            model_name='talkmessages',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.DeleteModel(
            name='CategoryTalk',
        ),
        migrations.DeleteModel(
            name='GeneralTalk',
        ),
        migrations.DeleteModel(
            name='SubjectTalk',
        ),
    ]
