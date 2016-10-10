# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uclptb', '0006_auto_20160914_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demographics',
            name='gp_practice_code',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='nhs_number',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
