# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0020_observations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observations',
            name='weight',
            field=models.FloatField(),
        ),
    ]
