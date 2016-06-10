# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uclptb', '0004_patientconsultation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patientconsultation',
            old_name='clinical_discussion',
            new_name='discussion',
        ),
        migrations.RemoveField(
            model_name='patientconsultation',
            name='discussed_with',
        ),
        migrations.AlterField(
            model_name='patientconsultation',
            name='reason_for_interaction_fk',
            field=models.ForeignKey(blank=True, to='opal.PatientConsultationReasonForInteraction', null=True),
        ),
    ]
