# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0023_auto_20160630_1340'),
        ('tb', '0008_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnvironmentalRiskAssessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('household', models.BooleanField(default=False)),
                ('shared_household', models.BooleanField(default=False)),
                ('prison', models.BooleanField(default=False)),
                ('homeless_hostel', models.BooleanField(default=False)),
                ('health_care_setting', models.BooleanField(default=False)),
                ('school_primary_and_above', models.BooleanField(default=False)),
                ('school_nursery', models.BooleanField(default=False)),
                ('congregate_drug_use', models.BooleanField(default=False)),
                ('pub_or_club', models.BooleanField(default=False)),
                ('other_setting', models.CharField(max_length=256, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_tb_environmentalriskassessment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_environmentalriskassessment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
    ]
