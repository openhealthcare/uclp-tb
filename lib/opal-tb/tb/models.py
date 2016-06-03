"""
Models for tb
"""
from django.db import models
from opal.models import EpisodeSubrecord


class TBRiskFactors(EpisodeSubrecord):
    previous_tb_where = models.CharField(max_length=255, blank=True)
    previous_tb_when = models.DateField(blank=True, null=True)
    previous_tb_how_long = models.CharField(max_length=255, blank=True)

    hiv_positive = models.NullBooleanField()
    type_1_diabetes = models.NullBooleanField()
    type_2_diabetes = models.NullBooleanField()
    known_tb_contact = models.NullBooleanField()
    bcg_history = models.NullBooleanField()
    bcg_scar_seen = models.NullBooleanField()

    recent_travel_to_high_risk_area = models.NullBooleanField()

    history_of_active_smoking = models.NullBooleanField()
    history_of_passive_field = models.NullBooleanField()
    referred_to_smoking_cessation = models.NullBooleanField()
    alcohol_misuse = models.NullBooleanField()
    no_recourse_to_public_funds = models.NullBooleanField()
