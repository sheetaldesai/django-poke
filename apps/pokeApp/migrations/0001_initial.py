# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 20:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('numPokesByPoker', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('alias', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=8)),
                ('birth_date', models.DateTimeField(verbose_name='date hired')),
                ('receivedPokes', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='pokes',
            name='poker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poked_by', to='pokeApp.Users'),
        ),
        migrations.AddField(
            model_name='pokes',
            name='reciever',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokes', to='pokeApp.Users'),
        ),
    ]
