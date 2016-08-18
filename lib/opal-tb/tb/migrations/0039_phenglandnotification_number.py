# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0038_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='phenglandnotification',
            name='number',
            field=models.CharField(max_length=250, null=True, verbose_name=b'LTBR Number', blank=True),
        ),
    ]
