# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-14 02:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20181112_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='restore',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='res', to='app.Comment', verbose_name='回复对象'),
        ),
    ]
