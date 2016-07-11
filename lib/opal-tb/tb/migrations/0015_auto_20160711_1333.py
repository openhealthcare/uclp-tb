# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0023_auto_20160630_1340'),
        ('tb', '0014_auto_20160711_0859'),
    ]

    operations = [
        migrations.CreateModel(
            name='PHEnglandNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('who', models.CharField(max_length=250, null=True, blank=True)),
                ('when', models.DateField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_tb_phenglandnotification_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_phenglandnotification_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='pheenglandnotification',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='pheenglandnotification',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='pheenglandnotification',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='PHEEnglandNotification',
        ),
    ]
