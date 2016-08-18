"""
tb models.
"""
from datetime import datetime, date

from django.db import models as fields
from django.db import models, transaction
from django.contrib.contenttypes.models import ContentType

from opal import models
from opal.core.lookuplists import LookupList

from tb.episode_categories import TBEpisode, TBEpisodeStages
from opal.core.fields import ForeignKeyOrFreeText
from opal.core import lookuplists, subrecords

class TBMeta(models.EpisodeSubrecord):
    _is_singleton = True
    _advanced_searchable = False

    contact_tracing_done = fields.BooleanField(default=False)
    directly_observed_therapy = fields.BooleanField(default=False)


class ContactDetails(models.PatientSubrecord):
    _is_singleton = True
    _advanced_searchable = False
    _icon = 'fa fa-phone'
    _title = 'Contact Details'

    telephone = fields.CharField(blank=True, null=True, max_length=50)
    address = fields.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Contact details"

class RelationshipToIndex(lookuplists.LookupList):
    pass


class ReasonAtRisk(lookuplists.LookupList):
    pass


class ContactTraced(models.EpisodeSubrecord):
    """ contact traced is the other side of the
        contact tracing relationship.

        this in theory has a 1 to many relationship between contact tracing
        ie we dont' create a contact traced if one already exists
        for the current episode.

        this includes things like, phoned, contacted, appointment booked
    """
    _title="Index Case"
    _icon = 'fa fa-street-view'
    symptomatic = fields.BooleanField(default=False)

    def to_dict(self, user):
        response = super(ContactTraced, self).to_dict(user)
        contact_tracing = []

        for i in self.contacttracing_set.all():
            contact_tracing.append(dict(
                episode=i.episode.to_dict(user),
                contact_tracing=i.to_dict(user)
            ))

        response["contact_tracing"] = contact_tracing
        return response


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
    _title="Contacts"
    _icon = 'fa fa-group'
    contact_traced = fields.ForeignKey(
        ContactTraced,
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
        schema = Demographics.build_field_schema()
        schema.extend(super(ContactTracing, cls).build_field_schema())
        schema.extend(ContactDetails.build_field_schema())

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
            patient = self.contact_traced.episode.patient
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
            stage=TBEpisodeStages.NEW_CONTACT,
            date_of_admission=date.today()
        )

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

    def create_contact_traced(self, data, episode):
        return ContactTraced.objects.create(
            episode=episode,
            symptomatic=data.get("symptomatic", False),
        )

    @transaction.atomic()
    def update_from_dict(self, data, user, *args, **kwargs):
        patient, created = self.get_or_create_patient(data, user)

        if created:
            episode = self.create_tb_episode(patient)
            self.contact_traced = self.create_contact_traced(data, episode)
            self.update_contact_details(patient, data, user)
            self.create_referral_route(self.contact_traced.episode, user)

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
        result = self.contact_traced.episode.patient.demographics_set.first().to_dict(user)
        result.update(self.contact_traced.episode.patient.contactdetails_set.first().to_dict(user))
        result.update(super(ContactTracing, self).to_dict(user))
        result["stage"] = self.contact_traced.episode.stage
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
    number = fields.CharField(max_length=250, blank=True, null=True, verbose_name="LTBR Number")


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

class TBHistory(models.PatientSubrecord):
    _icon = 'fa fa-wpforms'
    _title = "History of TB"
    personal_history_of_tb = fields.TextField(blank=True, null=True, verbose_name="Personal History of TB")
    other_tb_contact = fields.TextField(blank=True, null=True, verbose_name="Other TB Contact")
    date_of_other_tb_contact = fields.DateField(blank=True, null=True, verbose_name="When")

class BCG(models.PatientSubrecord):
    _icon = 'fa fa-asterisk'
    history_of_bcg = fields.CharField(max_length=255, blank=True, null=True, verbose_name="History Of BCG")
    date_of_bcg = fields.DateField(blank=True, null=True, verbose_name="Date Of BCG")
    bcg_scar = fields.BooleanField(default=False, verbose_name="BCG Scar")
    red_book_documentation_of_bcg_seen = fields.BooleanField(default=False, verbose_name="Red Book Documentation of BCG Seen")
