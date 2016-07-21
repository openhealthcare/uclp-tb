# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0026_auto_20160721_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbtests',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='tbtests',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='tbtests',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='TBTests',
        ),
    ]
