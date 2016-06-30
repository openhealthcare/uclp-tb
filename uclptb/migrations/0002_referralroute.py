# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0023_auto_20160630_1340'),
        ('uclptb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('internal', models.NullBooleanField()),
                ('referral_name', models.CharField(max_length=255, blank=True)),
                ('date_of_referral', models.DateField(null=True, blank=True)),
                ('referral_team_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('referral_organisation_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('referral_type_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_uclptb_referralroute_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('referral_organisation_fk', models.ForeignKey(blank=True, to='opal.ReferralOrganisation', null=True)),
                ('referral_team_fk', models.ForeignKey(blank=True, to='opal.Speciality', null=True)),
                ('referral_type_fk', models.ForeignKey(blank=True, to='opal.ReferralType', null=True)),
                ('updated_by', models.ForeignKey(related_name='updated_uclptb_referralroute_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
    ]
