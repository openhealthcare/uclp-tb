# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uclptb', '0003_referralroute'),
    ]

    operations = [
        migrations.RenameField(
            model_name='environmentaltbriskfactors',
            old_name='currentl_prison_stay',
            new_name='current_prison_stay',
        ),
    ]
