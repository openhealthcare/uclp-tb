# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0020_referralorganisation_referralreason'),
        ('uclptb', '0003_symptomcomplex'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientConsultation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('when', models.DateTimeField(null=True, blank=True)),
                ('initials', models.CharField(max_length=255, blank=True)),
                ('clinical_discussion', models.TextField(blank=True)),
                ('discussed_with', models.CharField(max_length=255, blank=True)),
                ('reason_for_interaction_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_uclptb_patientconsultation_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('reason_for_interaction_fk', models.ForeignKey(blank=True, to='opal.Clinical_advice_reason_for_interaction', null=True)),
                ('updated_by', models.ForeignKey(related_name='updated_uclptb_patientconsultation_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
    ]
