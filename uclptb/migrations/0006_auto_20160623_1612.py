# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uclptb', '0005_auto_20160610_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactdetails',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='ContactDetails',
        ),
    ]
