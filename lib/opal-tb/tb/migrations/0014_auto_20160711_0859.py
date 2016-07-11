# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0013_auto_20160708_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReasonAtRisk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RelationshipToIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='contacttracing',
            name='reason_at_risk_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contacttracing',
            name='relationship_to_index_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contacttracing',
            name='reason_at_risk_fk',
            field=models.ForeignKey(blank=True, to='tb.ReasonAtRisk', null=True),
        ),
        migrations.AddField(
            model_name='contacttracing',
            name='relationship_to_index_fk',
            field=models.ForeignKey(blank=True, to='tb.RelationshipToIndex', null=True),
        ),
    ]
