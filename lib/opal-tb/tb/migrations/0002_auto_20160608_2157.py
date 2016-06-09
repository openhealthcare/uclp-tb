# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='environmentaltbriskfactors',
            name='last_date_of_alcohol_misuse',
        ),
        migrations.RemoveField(
            model_name='environmentaltbriskfactors',
            name='last_date_of_homelessness',
        ),
        migrations.RemoveField(
            model_name='environmentaltbriskfactors',
            name='last_date_of_prison',
        ),
        migrations.RemoveField(
            model_name='environmentaltbriskfactors',
            name='last_date_of_problem_drug_use',
        ),
        migrations.AddField(
            model_name='environmentaltbriskfactors',
            name='last_year_of_alcohol_misuse',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='environmentaltbriskfactors',
            name='last_year_of_homelessness',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='environmentaltbriskfactors',
            name='last_year_of_prison',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='environmentaltbriskfactors',
            name='last_year_of_problem_drug_use',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
