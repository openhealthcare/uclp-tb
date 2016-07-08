# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0023_auto_20160630_1340'),
        ('tb', '0008_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodCulture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('lab_number', models.CharField(max_length=255, blank=True)),
                ('date_ordered', models.DateField(null=True, blank=True)),
                ('date_positive', models.DateField(null=True, blank=True)),
                ('source_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_tb_bloodculture_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BloodCultureIsolate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('aerobic', models.BooleanField()),
                ('FISH', models.ForeignKey(related_name='blood_culture_fish_organisms', blank=True, to='opal.Microbiology_organism', null=True)),
                ('blood_culture', models.ForeignKey(related_name='isolates', to='tb.BloodCulture')),
                ('created_by', models.ForeignKey(related_name='created_tb_bloodcultureisolate_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('microscopy', models.ForeignKey(related_name='blood_culture_microscopy_organisms', blank=True, to='opal.Microbiology_organism', null=True)),
                ('organism', models.ForeignKey(related_name='blood_culture_isolate_organisms', blank=True, to='opal.Microbiology_organism', null=True)),
                ('resistant_antibiotics', models.ManyToManyField(related_name='blood_culture_resistant', to='opal.Antimicrobial')),
                ('sensitive_antibiotics', models.ManyToManyField(related_name='blood_culture_sensitive', to='opal.Antimicrobial')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_bloodcultureisolate_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BloodCultureSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bloodculture',
            name='source_fk',
            field=models.ForeignKey(blank=True, to='tb.BloodCultureSource', null=True),
        ),
        migrations.AddField(
            model_name='bloodculture',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_tb_bloodculture_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
