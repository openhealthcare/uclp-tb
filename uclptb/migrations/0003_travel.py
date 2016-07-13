# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0023_auto_20160630_1340'),
        ('uclptb', '0002_referralroute'),
    ]

    operations = [
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('dates', models.CharField(max_length=255, blank=True)),
                ('specific_exposures', models.CharField(max_length=255, blank=True)),
                ('destination_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('reason_for_travel_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_uclptb_travel_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('destination_fk', models.ForeignKey(blank=True, to='opal.Destination', null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('reason_for_travel_fk', models.ForeignKey(blank=True, to='opal.Travel_reason', null=True)),
                ('updated_by', models.ForeignKey(related_name='updated_uclptb_travel_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
    ]
