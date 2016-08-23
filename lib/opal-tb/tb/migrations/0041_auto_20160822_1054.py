# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0040_auto_20160817_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbhistory',
            name='date_of_other_tb_contact',
        ),
        migrations.AddField(
            model_name='phenglandnotification',
            name='number',
            field=models.CharField(max_length=250, null=True, verbose_name=b'LTBR Number', blank=True),
        ),
        migrations.AlterField(
            model_name='bcg',
            name='bcg_scar',
            field=models.BooleanField(default=False, verbose_name=b'BCG Scar'),
        ),
        migrations.AlterField(
            model_name='bcg',
            name='date_of_bcg',
            field=models.DateField(null=True, verbose_name=b'Date Of BCG', blank=True),
        ),
        migrations.AlterField(
            model_name='bcg',
            name='history_of_bcg',
            field=models.CharField(max_length=255, null=True, verbose_name=b'History Of BCG', blank=True),
        ),
        migrations.AlterField(
            model_name='tbhistory',
            name='personal_history_of_tb',
            field=models.TextField(null=True, verbose_name=b'Personal History of TB', blank=True),
        ),
    ]
