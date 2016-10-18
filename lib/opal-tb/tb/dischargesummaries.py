"""
Discharge summary template for TB
"""
from dischargesummary import DischargeTemplate


class StartingActiveTBTreatment(DischargeTemplate):
    name = 'start_active_treatment'
    template = 'start_active_tb_letter.html'
    button_display = 'Start Active Treatment Letter'


class EndingActiveTBTreatment(DischargeTemplate):
    name = 'end_active_treatment'
    template = 'end_active_tb_letter.html'
    button_display = 'End Active Treatment Letter'


class MidActiveTBTreatment(DischargeTemplate):
    name = 'mid_active_treatment'
    template = 'mid_active_tb_letter.html'
    button_display = 'Mid Active Treatment Letter'


class LatentTBScrening(DischargeTemplate):
    name = 'latent_tb_screening'
    template = 'latent_tb_letter.html'
    button_display = 'Screening for LTBI Letter'
