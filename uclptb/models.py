"""
uclptb models.
"""
from django.db import models as fields

import opal.models as omodels

from opal.models import EpisodeSubrecord
from opal.core.fields import ForeignKeyOrFreeText

from opal import models

class Demographics(models.Demographics): pass
class Location(models.Location): pass
class Allergies(models.Allergies): pass
class Diagnosis(models.Diagnosis): pass
class PastMedicalHistory(models.PastMedicalHistory): pass

class Investigation(models.Investigation):
    genexpert = fields.CharField(max_length=255, blank=True, null=True)
    smear = fields.CharField(max_length=255, blank=True, null=True)
    culture = fields.CharField(max_length=255, blank=True, null=True)

class ReferralRoute(models.ReferralRoute): pass
class SymptomComplex(models.SymptomComplex): pass
class PatientConsultation(models.PatientConsultation): pass

class Treatment(models.Treatment):
    _angular_service = 'TreatmentRecord'
    planned_end_date = fields.DateField(blank=True, null=True)

class Travel(EpisodeSubrecord):
    _icon = 'fa fa-plane'

    destination         = ForeignKeyOrFreeText(omodels.Destination)
    dates               = fields.CharField(max_length=255, blank=True)
    reason_for_travel   = ForeignKeyOrFreeText(omodels.Travel_reason)
    specific_exposures  = fields.CharField(max_length=255, blank=True)
