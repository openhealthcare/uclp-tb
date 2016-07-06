# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0006_socialhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacttracing',
            name='contact_episode',
            field=models.ForeignKey(related_name='contact_traced', to='opal.Episode'),
        ),
    ]
