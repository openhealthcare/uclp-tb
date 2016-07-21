# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0021_auto_20160718_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phenglandnotification',
            name='when',
            field=models.DateField(null=True, verbose_name=b'Notification date', blank=True),
        ),
        migrations.AlterField(
            model_name='phenglandnotification',
            name='who',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Notified by', blank=True),
        ),
        migrations.AlterField(
            model_name='socialhistory',
            name='drinking',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Alcohol', blank=True),
        ),
    ]
