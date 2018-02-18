# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-18 22:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analytic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shortener.Smpl')),
            ],
        ),
    ]
