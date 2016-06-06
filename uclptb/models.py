"""
uclptb models.
"""
from django.db.models import fields

from opal import models

class Demographics(models.Demographics): pass
class Location(models.Location): pass
class Allergies(models.Allergies): pass
class Diagnosis(models.Diagnosis): pass
class PastMedicalHistory(models.PastMedicalHistory): pass
class Treatment(models.Treatment): pass
class Investigation(models.Investigation): pass


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


    last_date_of_problem_drug_use = fields.DateField(null=True, blank=True)
    current_problem_drug_use = fields.NullBooleanField()

    last_date_of_alcohol_misuse = fields.DateField(null=True, blank=True)
    current_alcohol_misuse = fields.NullBooleanField()

    last_date_of_homelessness = fields.DateField(null=True, blank=True)
    current_homelessness = fields.NullBooleanField()

    last_date_of_prison = fields.DateField(null=True, blank=True)
    currentl_prison_stay = fields.NullBooleanField()

    history_of_smoking_active = fields.NullBooleanField()
    history_of_smoking_passive = fields.NullBooleanField()

    recent_travel_to_high_risk_area = fields.NullBooleanField()


class MedicalTBRiskFactors(models.PatientSubrecord):
    _is_singleton = True


    mental_health_history = fields.NullBooleanField()
    previous_tb = fields.DateField(null=True, blank=True)

    hiv_positive = fields.NullBooleanField()
    solid_organ_transplantation = fields.NullBooleanField()

    haemotological_malignancy = fields.NullBooleanField()
    jejunoileal_bypass = fields.NullBooleanField()
    gastrectomy = fields.NullBooleanField()
    diabetes = fields.NullBooleanField()

    silicosis = fields.NullBooleanField()
    chronic_renal = fields.NullBooleanField()

    failure_haemodialysis = fields.NullBooleanField()

    anti_tnf_alpha_treatment = fields.NullBooleanField()
    other_immunosuppressive_drugs = fields.TextField()
