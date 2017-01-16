# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import opal.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0026_auto_20161120_2005'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BCG',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('history_of_bcg', models.CharField(max_length=255, null=True, verbose_name=b'History Of BCG', blank=True)),
                ('date_of_bcg', models.DateField(null=True, verbose_name=b'Date Of BCG', blank=True)),
                ('bcg_scar', models.BooleanField(default=False, verbose_name=b'BCG Scar')),
                ('red_book_documentation_of_bcg_seen', models.BooleanField(default=False, verbose_name=b'Red Book Documentation of BCG Seen')),
                ('created_by', models.ForeignKey(related_name='created_tb_bcg_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_bcg_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ContactDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('telephone', models.CharField(max_length=50, null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_tb_contactdetails_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_contactdetails_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Contact details',
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ContactTraced',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('symptomatic', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='created_tb_contacttraced_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_contacttraced_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ContactTracing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('relationship_to_index_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('reason_at_risk_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('contact_traced', models.ForeignKey(to='tb.ContactTraced')),
                ('created_by', models.ForeignKey(related_name='created_tb_contacttracing_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='EnvironmentalRiskAssessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('household', models.BooleanField(default=False)),
                ('shared_household', models.BooleanField(default=False)),
                ('prison', models.BooleanField(default=False)),
                ('homeless_hostel', models.BooleanField(default=False)),
                ('health_care_setting', models.BooleanField(default=False)),
                ('school_primary_and_above', models.BooleanField(default=False)),
                ('school_nursery', models.BooleanField(default=False)),
                ('congregate_drug_use', models.BooleanField(default=False)),
                ('pub_or_club', models.BooleanField(default=False)),
                ('other_setting', models.CharField(max_length=256, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_tb_environmentalriskassessment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_environmentalriskassessment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ObservedTreatment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('date', models.DateField()),
                ('initials', models.CharField(max_length=255, blank=True)),
                ('dose', models.CharField(max_length=255, blank=True)),
                ('observed', models.NullBooleanField()),
                ('drug_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_tb_observedtreatment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('drug_fk', models.ForeignKey(blank=True, to='opal.Drug', null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_observedtreatment_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PHEnglandNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('who', models.CharField(max_length=250, null=True, verbose_name=b'Notified by', blank=True)),
                ('when', models.DateField(null=True, verbose_name=b'Notification date', blank=True)),
                ('number', models.CharField(max_length=250, null=True, verbose_name=b'LTBR Number', blank=True)),
                ('created_by', models.ForeignKey(related_name='created_tb_phenglandnotification_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_phenglandnotification_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PossibleTBOutcome',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReasonAtRisk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RelationshipToIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SocialHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('notes', models.TextField(null=True, blank=True)),
                ('drinking', models.CharField(max_length=250, null=True, verbose_name=b'Alcohol', blank=True)),
                ('alcohol_dependent', models.NullBooleanField()),
                ('smoking', models.CharField(max_length=250, null=True, blank=True)),
                ('occupation', models.TextField(null=True, blank=True)),
                ('homelessness', models.TextField(null=True, blank=True)),
                ('intravenous_drug_use', models.CharField(max_length=250, null=True, blank=True)),
                ('incarceration', models.CharField(max_length=250, null=True, blank=True)),
                ('arrival_in_the_uk', models.CharField(max_length=250, null=True, verbose_name=b'Year of arrival', blank=True)),
                ('created_by', models.ForeignKey(related_name='created_tb_socialhistory_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_socialhistory_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TBHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('personal_history_of_tb', models.TextField(null=True, verbose_name=b'Personal History of TB', blank=True)),
                ('date_of_previous_tb_infection', models.CharField(max_length=255, null=True, verbose_name=b'Date of Previous TB', blank=True)),
                ('other_tb_contact', models.TextField(null=True, verbose_name=b'Other TB Contact', blank=True)),
                ('date_of_other_tb_contact', models.CharField(max_length=255, null=True, verbose_name=b'Date of TB Contact', blank=True)),
                ('created_by', models.ForeignKey(related_name='created_tb_tbhistory_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('patient', models.ForeignKey(to='opal.Patient')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_tbhistory_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TBLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('created_by', models.ForeignKey(related_name='created_tb_tblocation_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TBMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('contact_tracing_done', models.BooleanField(default=False)),
                ('directly_observed_therapy', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(related_name='created_tb_tbmeta_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('updated_by', models.ForeignKey(related_name='updated_tb_tbmeta_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TBOutcome',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('additional_details', models.TextField(null=True, blank=True)),
                ('outcome_ft', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='created_tb_tboutcome_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('outcome_fk', models.ForeignKey(blank=True, to='tb.PossibleTBOutcome', null=True)),
                ('updated_by', models.ForeignKey(related_name='updated_tb_tboutcome_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TBSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('name', models.CharField(max_length=255)),
                ('date_ordered', models.DateField(null=True, blank=True)),
                ('date_received', models.DateField(null=True, blank=True)),
                ('status', models.CharField(default=b'Pending', max_length=255)),
                ('result', models.TextField(null=True, blank=True)),
                ('mdr', models.BooleanField(default=False, verbose_name=b'MDR')),
                ('created_by', models.ForeignKey(related_name='created_tb_testresult_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('episode', models.ForeignKey(to='opal.Episode')),
                ('resistant_antibiotics', models.ManyToManyField(related_name='test_result_resistant', to='opal.Antimicrobial', blank=True)),
                ('sensitive_antibiotics', models.ManyToManyField(related_name='test_result_sensitive', to='opal.Antimicrobial', blank=True)),
                ('updated_by', models.ForeignKey(related_name='updated_tb_testresult_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.AddField(
            model_name='tblocation',
            name='sites',
            field=models.ManyToManyField(to='tb.TBSite', blank=True),
        ),
        migrations.AddField(
            model_name='tblocation',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_tb_tblocation_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='contacttracing',
            name='reason_at_risk_fk',
            field=models.ForeignKey(blank=True, to='tb.ReasonAtRisk', null=True),
        ),
        migrations.AddField(
            model_name='contacttracing',
            name='relationship_to_index_fk',
            field=models.ForeignKey(blank=True, to='tb.RelationshipToIndex', null=True),
        ),
        migrations.AddField(
            model_name='contacttracing',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_tb_contacttracing_subrecords', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
