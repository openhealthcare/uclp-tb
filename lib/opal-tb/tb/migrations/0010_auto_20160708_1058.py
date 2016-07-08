# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0009_tboutcome'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tboutcome',
            old_name='clincal_resolution',
            new_name='clinical_resolution',
        ),
    ]
