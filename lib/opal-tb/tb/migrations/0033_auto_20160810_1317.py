# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0032_auto_20160809_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactdetails',
            name='address_line1',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='address_line2',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='city',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='county',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='post_code',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='tel1',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='tel2',
        ),
        migrations.RemoveField(
            model_name='contacttraced',
            name='address',
        ),
        migrations.RemoveField(
            model_name='contacttraced',
            name='telephone',
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='address',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='telephone',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
