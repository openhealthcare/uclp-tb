# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0030_socialhistory_arrival_in_the_uk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='observations',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='observations',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='observations',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='Observations',
        ),
    ]
