"""
tb models.
"""
from django.db.models import fields

from opal import models


class EnvironmentalTBRiskFactors(models.PatientSubrecord):
    _is_singleton = True
    _title = "Environmental Risk Factors"
    _icon = 'fa fa-photo'


    last_date_of_problem_drug_use = fields.DateField(null=True, blank=True)
    current_problem_drug_use = fields.NullBooleanField()

    last_date_of_alcohol_misuse = fields.DateField(null=True, blank=True)
    current_alcohol_misuse = fields.NullBooleanField()

    last_date_of_homelessness = fields.DateField(null=True, blank=True)
    current_homelessness = fields.NullBooleanField()

    last_date_of_prison = fields.DateField(null=True, blank=True)
    current_prison_stay = fields.NullBooleanField()

    history_of_smoking_active = fields.NullBooleanField()
    history_of_smoking_passive = fields.NullBooleanField()

    recent_travel_to_high_risk_area = fields.NullBooleanField()


class MedicalTBRiskFactors(models.PatientSubrecord):
    _is_singleton = True
    _title = "Medical Risk Factors"
    _icon = 'fa fa-h-square'


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
