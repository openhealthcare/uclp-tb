"""
tb models.
"""
from datetime import datetime, date

from django.db import models as fields
from django.db import models, transaction
from django.contrib.contenttypes.models import ContentType

from opal import models
from opal.core.lookuplists import LookupList

from tb.episode_categories import TBEpisode
from opal.core.fields import ForeignKeyOrFreeText
from opal.core import lookuplists, subrecords

class TBMeta(models.EpisodeSubrecord):
    _is_singleton = True
    _advanced_searchable = False

    contact_tracing_done = fields.BooleanField(default=False)


class ContactDetails(models.PatientSubrecord):
    _is_singleton = True
    _advanced_searchable = False
    _icon = 'fa fa-phone'
    _title = 'Contact Details'

    address_line1 = fields.CharField("Address line 1", max_length = 45,
                                     blank=True, null=True)
    address_line2 = fields.CharField("Address line 2", max_length = 45,
                                     blank=True, null=True)
    city          = fields.CharField(max_length = 50, blank = True)
    county        = fields.CharField("County", max_length = 40,
                                     blank=True, null=True)
    post_code     = fields.CharField("Post Code", max_length = 10,
                                     blank=True, null=True)
    tel1          = fields.CharField(verbose_name="Telephone 1", blank=True, null=True, max_length=50)
    tel2          = fields.CharField(verbose_name="Telephone 2", blank=True, null=True, max_length=50)

    class Meta:
        verbose_name_plural = "Contact details"

class RelationshipToIndex(lookuplists.LookupList):
    pass


class ReasonAtRisk(lookuplists.LookupList):
    pass


class ContactTracing(models.EpisodeSubrecord):
    """ contact tracing works by having 2 sub models
        essentially demographics and contact details
        when we serialise the contact tracing
        we include the serialised fields of these models

        when we update contact tracing we get the models
        if they exist by looking at patient_id and episode_id
        and as these models are singletons this always
        gets us what we want
    """
    _icon = 'fa fa-group'
    contact_episode = fields.ForeignKey(
        models.Episode,
        related_name="contact_traced"
    )

    relationship_to_index = ForeignKeyOrFreeText(
        RelationshipToIndex,
    )
    reason_at_risk = ForeignKeyOrFreeText(
        ReasonAtRisk, verbose_name="reason for considering at risk"
    )

    @classmethod
    def build_field_schema(cls):
        Demographics = subrecords.get_subrecord_from_model_name('Demographics')
        ContactDetails = subrecords.get_subrecord_from_model_name('ContactDetails')
        schema = Demographics.build_field_schema()
        schema.extend(ContactDetails.build_field_schema())
        schema.extend(super(ContactTracing, cls).build_field_schema())

        schema.append({
            'name': "stage",
            'title': "Stage",
            'type': "string",
            'lookup_list': None,
            'model': cls.__name__
        })

        return schema

    def get_or_create_patient(self, data, user):
        if self.id:
            created = False
            patient = self.contact_episode.patient
        else:
            created = True
            patient = models.Patient.objects.create()
            Demographics = subrecords.get_subrecord_from_model_name('Demographics')
            demographics = patient.demographics_set.first()
            demographics_fields = Demographics._get_fieldnames_to_serialize()
            demographics_data = {
                i: v for i, v in data.iteritems() if i in demographics_fields and not i == "id" and not i == "patient_id"
            }
            demographics.update_from_dict(demographics_data, user)

        return patient, created

    def update_contact_details(self, patient, data, user):
        """
        current behaviour is if there are no contact details
        we'll let you populate them, otherwise they'll stay the same
        """
        ContactDetails = subrecords.get_subrecord_from_model_name('ContactDetails')
        contact_details_fields = ContactDetails._get_fieldnames_to_serialize()
        contact_details = patient.contactdetails_set.first()
        contact_detail_data = {
            i: v for i, v in data.iteritems() if i in contact_details_fields and not i == "id" and not i == "patient_id"
        }
        contact_details.update_from_dict(contact_detail_data, user)

    def get_episode(self, patient):
        tb_episodes = patient.episode_set.filter(category_name=TBEpisode.get_slug())

        for tb_episode in tb_episodes:
            if not tb_episode.end:
                return tb_episode

    def create_referral_route(self, episode, user):
        referral = episode.referralroute_set.first()
        referral.referral_type = "TB contact tracing"
        referral.date_of_referral = date.today()
        referral.internal = True
        referral.referral_organisation = "TB Clinic"
        if user.first_name and user.last_name:
            referral_name = "{} {}".format(user.first_name[:1], user.last_name)
            referral.referral_name = referral_name
        referral.save()

    def create_tb_episode(self, patient):
        return patient.create_episode(
            category_name=TBEpisode.get_slug().upper(),
            stage=TBEpisode.stages.CONTACT_TRACING,
            date_of_admission=date.today()
        )

    @transaction.atomic()
    def update_from_dict(self, data, user, *args, **kwargs):
        patient, created = self.get_or_create_patient(data, user)

        if created:
            self.update_contact_details(patient, data, user)
            self.contact_episode = self.create_tb_episode(patient)
            self.create_referral_route(self.contact_episode, user)

        self.relationship_to_index = data.pop("relationship_to_index", None)
        self.reason_at_risk = data.pop("reason_at_risk", None)
        self.set_created_by_id(data, user)
        self.set_updated_by_id(data, user)
        self.set_updated(data, user)
        self.set_created(data, user)
        self.save()

    def to_dict(self, user):
        """
            to dict is an aggregate serialisation
            of patient, contact details and
            episode stage
        """
        result = self.contact_episode.patient.demographics_set.first().to_dict(user)
        result.update(self.contact_episode.patient.contactdetails_set.first().to_dict(user))
        result.update(super(ContactTracing, self).to_dict(user))
        result["stage"] = self.contact_episode.stage
        return result


class SocialHistory(models.EpisodeSubrecord):
    _is_singleton = True
    _title = 'Social History'
    _icon = 'fa fa-clock-o'

    notes             = fields.TextField(blank=True, null=True)
    drinking          = fields.CharField(max_length=250, blank=True, null=True, verbose_name="Alcohol")
    alcohol_dependent = fields.NullBooleanField()
    smoking           = fields.CharField(max_length=250, blank=True, null=True)
    occupation        = fields.TextField(blank=True, null=True)
    homelessness      = fields.TextField(blank=True, null=True)
    intravenous_drug_use = fields.CharField(max_length=250, blank=True, null=True)
    incarceration = fields.CharField(max_length=250, blank=True, null=True)
    arrival_in_the_uk = fields.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Year of arrival"
    )


def get_for_lookup_list(model, values):
    ct = ContentType.objects.get_for_model(model)
    return model.objects.filter(
        models.Q(name__in=values) |
        models.Q(synonyms__name__in=values, synonyms__content_type=ct)
    )

class PHEnglandNotification(models.EpisodeSubrecord):
    _title = "Public Health Notification"
    _is_singleton = True
    _icon = 'fa fa-flag'

    who = fields.CharField(max_length=250, blank=True, null=True, verbose_name="Notified by")
    when = fields.DateField(null=True, blank=True, verbose_name="Notification date")


class TBOutcome(models.EpisodeSubrecord):
    _is_singleton = True
    _title = 'TB Treatment Outcome'
    _icon = 'fa fa-th-list'

    clinical_resolution             = fields.NullBooleanField()
    radiological_resolution         = fields.NullBooleanField()
    clinical_resolution_details     = fields.TextField(blank=True, null=True)
    radiological_resolution_details = fields.TextField(blank=True, null=True)

class TBSite(LookupList):
    pass


class TBLocation(models.EpisodeSubrecord):
    sites = fields.ManyToManyField(TBSite)
    _is_singleton = True

    def to_dict(self, user):
        result = super(TBLocation, self).to_dict(user)
        result["sites"] = list(self.sites.values_list("name", flat=True))
        return result


class EnvironmentalRiskAssessment(models.EpisodeSubrecord):
    _is_singleton = True
    _title = 'Environmental Risk'
    _icon = 'fa fa-photo'

    household = fields.BooleanField(default=False)
    shared_household = fields.BooleanField(default=False)
    prison = fields.BooleanField(default=False)
    homeless_hostel = fields.BooleanField(default=False)
    health_care_setting = fields.BooleanField(default=False)
    school_primary_and_above = fields.BooleanField(default=False)
    school_nursery = fields.BooleanField(default=False)
    congregate_drug_use = fields.BooleanField(default=False)
    pub_or_club = fields.BooleanField(default=False)
    other_setting = fields.CharField(null=True, blank=True, max_length=256)


class TestResult(models.EpisodeSubrecord):
    _icon = 'fa fa-crosshairs'
    _title = "Tests"
    _angular_service = 'TestResultRecord'

    name = fields.CharField(max_length=255)
    date_ordered = fields.DateField(null=True, blank=True)
    date_received = fields.DateField(null=True, blank=True)
    status = fields.CharField(max_length=255, default="Pending")
    result = fields.TextField(null=True, blank=True)
    sensitive_antibiotics = fields.ManyToManyField(
        models.Antimicrobial, related_name="test_result_sensitive"
    )
    resistant_antibiotics = fields.ManyToManyField(
        models.Antimicrobial, related_name="test_result_resistant"
    )
