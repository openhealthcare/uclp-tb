# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0023_auto_20160630_1340'),
        ('tb', '0006_socialhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='TBRiskFactors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('hiv_status', models.CharField(max_length=250, null=True, blank=True)),
                ('diabetes', models.CharField(max_length=250, null=True, blank=True)),
                ('corticosteroid_therapy', models.NullBooleanField()),
                ('anti_tnf_alpha_treatment', models.NullBooleanField()),
                ('chronic_lung_disease', models.NullBooleanField()),
                ('created_by', models.ForeignKey(related_name='created_tb_tbriskfactors_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_tbriskfactors_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
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
            name='MedicalTBRiskFactors',
        ),
    ]
