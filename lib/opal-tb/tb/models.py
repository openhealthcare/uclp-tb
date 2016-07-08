"""
tb models.
"""
from django.db import models as fields
from django.db import models, transaction

from opal import models
from opal.core import subrecords, exceptions

from tb.episode_categories import TBEpisode


class ContactDetails(models.PatientSubrecord):
    _is_singleton = True
    _advanced_searchable = False
    _icon = 'fa fa-phone'

    address_line1 = fields.CharField("Address line 1", max_length = 45,
                                     blank=True, null=True)
    address_line2 = fields.CharField("Address line 2", max_length = 45,
                                     blank=True, null=True)
    city          = fields.CharField(max_length = 50, blank = True)
    county        = fields.CharField("County", max_length = 40,
                                     blank=True, null=True)
    post_code     = fields.CharField("Post Code", max_length = 10,
                                     blank=True, null=True)
    tel1          = fields.CharField(blank=True, null=True, max_length=50)
    tel2          = fields.CharField(blank=True, null=True, max_length=50)

    class Meta:
        verbose_name_plural = "Contact details"


class EnvironmentalTBRiskFactors(models.PatientSubrecord):
    _is_singleton = True
    _title = "Environmental Risk Factors"
    _icon = 'fa fa-photo'


    last_year_of_problem_drug_use = fields.CharField(max_length=20, blank=True, null=True)
    current_problem_drug_use = fields.NullBooleanField()

    last_year_of_alcohol_misuse = fields.CharField(max_length=20, blank=True, null=True)
    current_alcohol_misuse = fields.NullBooleanField()

    last_year_of_homelessness = fields.CharField(max_length=20, blank=True, null=True)
    current_homelessness = fields.NullBooleanField()

    last_year_of_prison = fields.CharField(max_length=20, blank=True, null=True)
    current_prison_stay = fields.NullBooleanField()

    history_of_smoking_active = fields.NullBooleanField()
    history_of_smoking_passive = fields.NullBooleanField()

    recent_travel_to_high_risk_area = fields.NullBooleanField()


# class MedicalTBRiskFactors(models.PatientSubrecord):
class TBRiskFactors(models.EpisodeSubrecord):
    _is_singleton = True
    _title = "TB Risk Factors"
    _icon = 'fa fa-warning'

    hiv_status               = fields.CharField(max_length=250, blank=True, null=True)
    diabetes                 = fields.CharField(max_length=250, blank=True, null=True)
    corticosteroid_therapy   = fields.NullBooleanField()
    anti_tnf_alpha_treatment = fields.NullBooleanField()
    chronic_lung_disease     = fields.NullBooleanField()

    # mental_health_history = fields.NullBooleanField()
    # previous_tb = fields.DateField(null=True, blank=True)
    # hiv_positive = fields.NullBooleanField()
    # solid_organ_transplantation = fields.NullBooleanField()
    # haemotological_malignancy = fields.NullBooleanField()
    # jejunoileal_bypass = fields.NullBooleanField()
    # gastrectomy = fields.NullBooleanField()
    # diabetes = fields.NullBooleanField()
    # silicosis = fields.NullBooleanField()
    # chronic_renal = fields.NullBooleanField()
    # failure_haemodialysis = fields.NullBooleanField()
    # other_immunosuppressive_drugs = fields.TextField()


class TBTests(models.EpisodeSubrecord):
    _is_singleton = True
    _title = "Tests"
    _icon = 'fa fa-laptop'

    sputum_1 = fields.BooleanField(default=False)
    sputum_2 = fields.BooleanField(default=False)
    sputum_3 = fields.BooleanField(default=False)
    sputum_pcr = fields.BooleanField(default=False)
    fna = fields.BooleanField(default=False)
    biopsy = fields.BooleanField(default=False)
    qftt_spot = fields.BooleanField(default=False)
    ct_scan = fields.BooleanField(default=False)
    routine_blood_tests = fields.BooleanField(default=False)
    chest_xray = fields.BooleanField(default=False)


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
        if self.contact_episode_id:
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

    def create_tb_episode(self, patient):
        return patient.create_episode(
            category_name=TBEpisode.get_slug().upper(),
            stage=TBEpisode.stages.CONTACT_TRACING
        )

    @transaction.atomic()
    def update_from_dict(self, data, user, *args, **kwargs):
        patient, created = self.get_or_create_patient(data, user)
        tb_episode = None

        if created:
            self.update_contact_details(patient, data, user)
            self.contact_episode = tb_episode = self.create_tb_episode(patient)

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
    drinking          = fields.CharField(max_length=250, blank=True, null=True)
    alcohol_dependent = fields.NullBooleanField()
    smoking           = fields.CharField(max_length=250, blank=True, null=True)
    occupation        = fields.TextField(blank=True, null=True)
    no_fixed_abode    = fields.NullBooleanField()


class TBOutcome(models.EpisodeSubrecord):
    _is_singleton = True
    _title = 'TB Treatment Outcome'
    _icon = 'fa fa-th-list'

    clinical_resolution              = fields.NullBooleanField()
    radiological_resolution         = fields.NullBooleanField()
    clinical_resolution_details     = fields.TextField(blank=True, null=True)
    radiological_resolution_details = fields.TextField(blank=True, null=True)


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
