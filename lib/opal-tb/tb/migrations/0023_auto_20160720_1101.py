# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0022_auto_20160720_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialhistory',
            name='homelessness',
            field=models.TextField(null=True, blank=True),
        ),
    ]
