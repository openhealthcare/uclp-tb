# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0015_auto_20160711_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloodculture',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='bloodculture',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='bloodculture',
            name='source_fk',
        ),
        migrations.RemoveField(
            model_name='bloodculture',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='bloodcultureisolate',
            name='FISH',
        ),
        migrations.RemoveField(
            model_name='bloodcultureisolate',
            name='blood_culture',
        ),
        migrations.RemoveField(
            model_name='bloodcultureisolate',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='bloodcultureisolate',
            name='microscopy',
        ),
        migrations.RemoveField(
            model_name='bloodcultureisolate',
            name='organism',
        ),
        migrations.RemoveField(
            model_name='bloodcultureisolate',
            name='resistant_antibiotics',
        ),
        migrations.RemoveField(
            model_name='bloodcultureisolate',
            name='sensitive_antibiotics',
        ),
        migrations.RemoveField(
            model_name='bloodcultureisolate',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='BloodCulture',
        ),
        migrations.DeleteModel(
            name='BloodCultureIsolate',
        ),
        migrations.DeleteModel(
            name='BloodCultureSource',
        ),
    ]
