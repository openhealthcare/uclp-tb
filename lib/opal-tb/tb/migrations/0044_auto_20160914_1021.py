# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lab', '__first__'),
        ('tb', '0043_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabTestCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('created_by', models.ForeignKey(related_name='created_tb_labtestcollection_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_labtestcollection_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Culture',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('lab.posneglabtest',),
        ),
        migrations.CreateModel(
            name='GeneXpert',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('lab.posneglabtest',),
        ),
        migrations.CreateModel(
            name='Smear',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('lab.labtest',),
        ),
        migrations.AlterField(
            model_name='tbhistory',
            name='date_of_previous_tb_infection',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Date of Previous TB', blank=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='mdr',
            field=models.BooleanField(default=False, verbose_name=b'MDR'),
        ),
    ]
