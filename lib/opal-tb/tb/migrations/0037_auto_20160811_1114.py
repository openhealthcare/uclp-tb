# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0036_bcg'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbhistory',
            name='date_of_other_tb_contact',
            field=models.DateField(null=True, verbose_name=b'When', blank=True),
        ),
        migrations.AlterField(
            model_name='bcg',
            name='red_book_documentation_of_bcg_seen',
            field=models.BooleanField(default=False, verbose_name=b'Red Book Documentation of BCG Seen'),
        ),
    ]
