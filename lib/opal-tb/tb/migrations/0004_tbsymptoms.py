# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0022_episode_stage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tb', '0003_lymphadenopathy_tbradiology'),
    ]

    operations = [
        migrations.CreateModel(
            name='TBSymptoms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('cough', models.BooleanField()),
                ('night_sweats', models.BooleanField()),
                ('fatigue', models.BooleanField()),
                ('fever', models.BooleanField()),
                ('chills', models.BooleanField()),
                ('loss_of_appetite', models.BooleanField()),
                ('weight_loss', models.BooleanField()),
                ('haemoptysis', models.BooleanField()),
                ('created_by', models.ForeignKey(related_name='created_tb_tbsymptoms_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_tbsymptoms_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
    ]
