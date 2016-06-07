# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import opal.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0019_auto_20160607_1039'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EnvironmentalTBRiskFactors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('last_date_of_problem_drug_use', models.DateField(null=True, blank=True)),
                ('current_problem_drug_use', models.NullBooleanField()),
                ('last_date_of_alcohol_misuse', models.DateField(null=True, blank=True)),
                ('current_alcohol_misuse', models.NullBooleanField()),
                ('last_date_of_homelessness', models.DateField(null=True, blank=True)),
                ('current_homelessness', models.NullBooleanField()),
                ('last_date_of_prison', models.DateField(null=True, blank=True)),
                ('current_prison_stay', models.NullBooleanField()),
                ('history_of_smoking_active', models.NullBooleanField()),
                ('history_of_smoking_passive', models.NullBooleanField()),
                ('recent_travel_to_high_risk_area', models.NullBooleanField()),
                ('created_by', models.ForeignKey(related_name='created_tb_environmentaltbriskfactors_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_environmentaltbriskfactors_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MedicalTBRiskFactors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('mental_health_history', models.NullBooleanField()),
                ('previous_tb', models.DateField(null=True, blank=True)),
                ('hiv_positive', models.NullBooleanField()),
                ('solid_organ_transplantation', models.NullBooleanField()),
                ('haemotological_malignancy', models.NullBooleanField()),
                ('jejunoileal_bypass', models.NullBooleanField()),
                ('gastrectomy', models.NullBooleanField()),
                ('diabetes', models.NullBooleanField()),
                ('silicosis', models.NullBooleanField()),
                ('chronic_renal', models.NullBooleanField()),
                ('failure_haemodialysis', models.NullBooleanField()),
                ('anti_tnf_alpha_treatment', models.NullBooleanField()),
                ('other_immunosuppressive_drugs', models.TextField()),
                ('created_by', models.ForeignKey(related_name='created_tb_medicaltbriskfactors_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_medicaltbriskfactors_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
    ]
