# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-25 13:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_root', '0004_auto_20170325_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='imdb_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
