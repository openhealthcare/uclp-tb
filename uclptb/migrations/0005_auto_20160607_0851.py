# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uclptb', '0004_auto_20160606_1422'),
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
            model_name='medicaltbriskfactors',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='medicaltbriskfactors',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='medicaltbriskfactors',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='EnvironmentalTBRiskFactors',
        ),
        migrations.DeleteModel(
            name='MedicalTBRiskFactors',
        ),
    ]
