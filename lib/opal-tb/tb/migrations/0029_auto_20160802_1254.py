# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0028_tbmeta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='environmentaltbriskfactors',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='environmentaltbriskfactors',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='environmentaltbriskfactors',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='tbriskfactors',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='tbriskfactors',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='tbriskfactors',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='EnvironmentalTBRiskFactors',
        ),
        migrations.DeleteModel(
            name='TBRiskFactors',
        ),
    ]
