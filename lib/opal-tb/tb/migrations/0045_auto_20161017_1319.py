# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0044_auto_20160914_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='PossibleTBOutcome',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='tboutcome',
            name='clinical_resolution',
        ),
        migrations.RemoveField(
            model_name='tboutcome',
            name='clinical_resolution_details',
        ),
        migrations.RemoveField(
            model_name='tboutcome',
            name='radiological_resolution',
        ),
        migrations.RemoveField(
            model_name='tboutcome',
            name='radiological_resolution_details',
        ),
        migrations.AddField(
            model_name='tboutcome',
            name='additional_details',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='tboutcome',
            name='outcome_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='tboutcome',
            name='outcome_fk',
            field=models.ForeignKey(blank=True, to='tb.PossibleTBOutcome', null=True),
        ),
    ]
