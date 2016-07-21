# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0025_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdetails',
            name='tel1',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Telephone 1', blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='tel2',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Telephone 2', blank=True),
        ),
    ]
