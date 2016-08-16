# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0030_socialhistory_arrival_in_the_uk'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbmeta',
            name='directly_observed_therapy',
            field=models.BooleanField(default=False),
        ),
    ]
