"""
tb models.
"""
from django.db.models import fields

from opal import models
from opal.core import fields as opal_fields
from opal.core import lookuplists


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


# class RadiologyScanType(lookuplists.LookupList):
#     pass
#
#
# class RadiologyScanResult(lookuplists.LookupList):
#     pass
#
#
# class Radiology(models.EpisodeSubrecord):
#     scan_type = opal_fields.ForeignKeyOrFreeText(RadiologyScanType)
#     scan_result = opal_fields.ForeignKeyOrFreeText(RadiologyScanResult)
#     comments = fields.TextField()

# ask in the tb channelf for how best to model this
