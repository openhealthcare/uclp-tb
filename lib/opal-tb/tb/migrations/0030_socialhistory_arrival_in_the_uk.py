# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0029_auto_20160802_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialhistory',
            name='arrival_in_the_uk',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Year of arrival', blank=True),
        ),
    ]
