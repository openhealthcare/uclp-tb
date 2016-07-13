# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0017_tbsite'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialhistory',
            name='incarceration',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='socialhistory',
            name='intravenous_drug_use',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
