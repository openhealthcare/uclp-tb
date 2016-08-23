# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0023_auto_20160630_1340'),
        ('tb', '0039_observedtreatment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='observedtreatment',
            name='treatement',
        ),
        migrations.AddField(
            model_name='observedtreatment',
            name='dose',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='observedtreatment',
            name='drug_fk',
            field=models.ForeignKey(blank=True, to='opal.Drug', null=True),
        ),
        migrations.AddField(
            model_name='observedtreatment',
            name='drug_ft',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='observedtreatment',
            name='observed',
            field=models.NullBooleanField(),
        ),
    ]
