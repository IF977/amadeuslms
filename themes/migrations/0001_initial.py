# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-06 19:14
from __future__ import unicode_literals

from django.db import migrations, models
import themes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Themes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Projeto Amadeus', max_length=200, verbose_name='Title')),
                ('small_logo', models.ImageField(blank=True, default='logo_pequena_amadeus.png', upload_to='themes/', validators=[themes.models.validate_img_extension], verbose_name='Small Logo')),
                ('large_logo', models.ImageField(blank=True, default='logo_grande_amadeus.png', upload_to='themes/', validators=[themes.models.validate_img_extension], verbose_name='Large Logo')),
                ('footer_note', models.TextField(blank=True, verbose_name='Footer Note')),
                ('css_style', models.CharField(default='green', max_length=50, verbose_name='Css Style')),
            ],
            options={
                'verbose_name': 'Theme',
                'verbose_name_plural': 'Themes',
            },
        ),
    ]
