# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0041_auto_20160822_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='mdr',
            field=models.BooleanField(default=False),
        ),
    ]
