# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 20:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokeApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokes',
            old_name='reciever',
            new_name='receiver',
        ),
    ]