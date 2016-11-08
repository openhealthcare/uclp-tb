# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uclptb', '0005_auto_20160728_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demographics',
            name='gp_practice_code',
            field=models.CharField(max_length=20, null=True, verbose_name=b'GP Practice Code', blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='nhs_number',
            field=models.CharField(max_length=255, null=True, verbose_name=b'NHS Number', blank=True),
        ),
    ]
