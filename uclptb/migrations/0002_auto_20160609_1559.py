# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0020_referralorganisation_referralreason'),
        ('uclptb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referralroute',
            name='referral_reason',
        ),
        migrations.RemoveField(
            model_name='referralroute',
            name='referral_route',
        ),
        migrations.RemoveField(
            model_name='referralroute',
            name='referral_team',
        ),
        migrations.AddField(
            model_name='referralroute',
            name='referral_organisation_fk',
            field=models.ForeignKey(blank=True, to='opal.ReferralOrganisation', null=True),
        ),
        migrations.AddField(
            model_name='referralroute',
            name='referral_organisation_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='referralroute',
            name='referral_reason_fk',
            field=models.ForeignKey(blank=True, to='opal.ReferralReason', null=True),
        ),
        migrations.AddField(
            model_name='referralroute',
            name='referral_reason_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='referralroute',
            name='referral_team_fk',
            field=models.ForeignKey(blank=True, to='opal.Speciality', null=True),
        ),
        migrations.AddField(
            model_name='referralroute',
            name='referral_team_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
    ]
