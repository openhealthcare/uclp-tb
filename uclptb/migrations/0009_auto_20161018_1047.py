# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uclptb', '0008_auto_20161017_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='investigation',
            name='culture',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='investigation',
            name='genexpert',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='investigation',
            name='smear',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
