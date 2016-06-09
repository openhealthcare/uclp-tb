from pathway.pathways import (
    ModalPathway, Pathway, RedirectsToPatientMixin, MultSaveStep
)
from uclptb.models import Demographics
from uclptb import models as uclptb_models
from tb import models as tb_models


class NextTBStage(ModalPathway):
    display_name = "Next TB Stage"
    slug = "next_tb_stage"

    steps = (Demographics,)


class TBScreening(RedirectsToPatientMixin, Pathway):
    display_name = "TB Screening"
    slug = "tb_screening"
    steps = (
        # uclptb_models.Demographics,
        # uclptb_models.ContactDetails,
        # uclptb_models.ReferralRoute,
        # tb_models.EnvironmentalTBRiskFactors,
        # tb_models.MedicalTBRiskFactors,
        MultSaveStep(model=uclptb_models.Investigation),
        MultSaveStep(model=uclptb_models.PastMedicalHistory),
    )
