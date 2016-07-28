# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uclptb', '0004_treatment_planned_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allergies',
            name='provisional',
            field=models.BooleanField(default=False, verbose_name=b'Suspected?'),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='provisional',
            field=models.BooleanField(default=False, verbose_name=b'Provisional?'),
        ),
    ]
