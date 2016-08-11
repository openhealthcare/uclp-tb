# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0023_auto_20160630_1340'),
        ('tb', '0035_auto_20160811_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='BCG',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('history_of_bcg', models.CharField(max_length=255, null=True, blank=True)),
                ('date_of_bcg', models.DateField(null=True, blank=True)),
                ('bcg_scar', models.BooleanField(default=False)),
                ('red_book_documentation_of_bcg_seen', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='created_tb_bcg_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_bcg_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
    ]
