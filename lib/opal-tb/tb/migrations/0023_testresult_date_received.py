# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0022_auto_20160720_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='date_received',
            field=models.DateField(null=True, blank=True),
        ),
    ]
