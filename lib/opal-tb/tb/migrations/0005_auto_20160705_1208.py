# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0023_auto_20160630_1340'),
        ('tb', '0004_contactdetails_contacttracing'),
    ]

    operations = [
        migrations.CreateModel(
            name='TBTests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('sputum_1', models.BooleanField(default=False)),
                ('sputum_2', models.BooleanField(default=False)),
                ('sputum_3', models.BooleanField(default=False)),
                ('sputum_pcr', models.BooleanField(default=False)),
                ('fna', models.BooleanField(default=False)),
                ('biopsy', models.BooleanField(default=False)),
                ('qftt_spot', models.BooleanField(default=False)),
                ('ct_scan', models.BooleanField(default=False)),
                ('routine_blood_tests', models.BooleanField(default=False)),
                ('chest_xray', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='created_tb_tbtests_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_tbtests_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='tbradiology',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='tbradiology',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='tbradiology',
            name='lymphadenopathy_fk',
        ),
        migrations.RemoveField(
            model_name='tbradiology',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='Lymphadenopathy',
        ),
        migrations.DeleteModel(
            name='TBRadiology',
        ),
    ]
