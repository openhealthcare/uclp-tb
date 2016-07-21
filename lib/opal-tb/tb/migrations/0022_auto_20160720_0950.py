# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0023_auto_20160630_1340'),
        ('tb', '0021_auto_20160718_1005'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('name', models.CharField(max_length=255)),
                ('date_ordered', models.DateField(null=True, blank=True)),
                ('status', models.CharField(default=b'Pending', max_length=255)),
                ('result', models.TextField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_tb_testresult_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('resistant_antibiotics', models.ManyToManyField(related_name='test_result_resistant', to='opal.Antimicrobial')),
                ('sensitive_antibiotics', models.ManyToManyField(related_name='test_result_sensitive', to='opal.Antimicrobial')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_testresult_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
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
