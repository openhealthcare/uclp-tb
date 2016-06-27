# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import opal.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0022_episode_stage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tb', '0003_lymphadenopathy_tbradiology'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('address_line1', models.CharField(max_length=45, null=True, verbose_name=b'Address line 1', blank=True)),
                ('address_line2', models.CharField(max_length=45, null=True, verbose_name=b'Address line 2', blank=True)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('county', models.CharField(max_length=40, null=True, verbose_name=b'County', blank=True)),
                ('post_code', models.CharField(max_length=10, null=True, verbose_name=b'Post Code', blank=True)),
                ('tel1', models.CharField(max_length=50, null=True, blank=True)),
                ('tel2', models.CharField(max_length=50, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_tb_contactdetails_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_contactdetails_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Contact details',
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ContactTracing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('contact_episode', models.ForeignKey(related_name='contract_traced', to='opal.Episode')),
                ('created_by', models.ForeignKey(related_name='created_tb_contacttracing_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_contacttracing_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
    ]
