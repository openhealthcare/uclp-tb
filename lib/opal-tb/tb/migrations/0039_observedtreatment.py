# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0023_auto_20160630_1340'),
        ('uclptb', '0005_auto_20160728_1528'),
        ('tb', '0038_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObservedTreatment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('date', models.DateField()),
                ('initials', models.CharField(max_length=255, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_tb_observedtreatment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('treatement', models.ForeignKey(to='uclptb.Treatment')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_observedtreatment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
    ]
