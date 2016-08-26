# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0041_auto_20160822_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbhistory',
            name='date_of_other_tb_contact',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Date of TB Contact', blank=True),
        ),
        migrations.AddField(
            model_name='tbhistory',
            name='date_of_previous_tb_infection',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Date of Previous TB Infection', blank=True),
        ),
    ]
