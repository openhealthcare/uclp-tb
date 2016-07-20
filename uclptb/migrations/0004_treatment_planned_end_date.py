# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uclptb', '0003_travel'),
    ]

    operations = [
        migrations.AddField(
            model_name='treatment',
            name='planned_end_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
