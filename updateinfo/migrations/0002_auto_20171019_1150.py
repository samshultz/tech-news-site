# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-19 10:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('updateinfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'ordering': ('name',)},
        ),
    ]
