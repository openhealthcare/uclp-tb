# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0031_auto_20160809_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacttraced',
            name='address',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contacttraced',
            name='symptomatic',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contacttraced',
            name='telephone',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
