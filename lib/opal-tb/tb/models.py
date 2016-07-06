"""
tb models.
"""
from django.db import models as fields
from django.db import models, transaction

from opal import models
from opal.core import subrecords

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
    _icon = 'fa fa-group'
    contact_episode = fields.ForeignKey(
        models.Episode,
        related_name="contract_traced"
    )

    def get_or_create_patient(self, data, user):
        Demographics = subrecords.get_subrecord_from_model_name('Demographics')
        demographics_fields = Demographics._get_fieldnames_to_serialize()
        demographics_data = {
            i: v for i, v in data.iteritems() if v and i in demographics_fields
        }

        filter_fields = [
            "first_name",
            "surname",
            "hospital_number",
            "nhs_number"
        ]

        filter_args = {
            i: v for i, v in demographics_data.iteritems() if v and i in filter_fields
        }

        demographics = Demographics.objects.filter(
            **filter_args
        ).first()

        if demographics:
            created = False
            patient = demographics.patient
        else:
            created = True
            patient = models.Patient.objects.create()
            demographics = patient.demographics_set.first()
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

        if not contact_details.updated:
            contact_detail_data = {
                i: v for i, v in data.iteritems() if i in contact_details_fields
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

        if not created:
            tb_episode = self.get_episode(patient)
            self.update_contact_details(patient, data, user)

        if not tb_episode:
            tb_episode = self.create_tb_episode(patient)

        self.contact_episode = tb_episode
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
        result = {
            "created": self.created,
            "stage": self.contact_episode.stage,
            "patient_id": self.contact_episode.patient.id,
            "episode_id": self.contact_episode.id
        }

        result.update(self.contact_episode.patient.demographics_set.first().to_dict(user))
        result.update(self.contact_episode.patient.contactdetails_set.first().to_dict(user))
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
