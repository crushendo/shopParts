# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-09 19:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_auto_20160609_1558'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CATEGORY',
            new_name='Part',
        ),
    ]
