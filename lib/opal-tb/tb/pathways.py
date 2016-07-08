"""
OPAL Pathway definitions for the re-usable TB module.
"""
from pathway import pathways
from pathway.pathways import (
    ModalPathway, Pathway, RedirectsToPatientMixin, MultSaveStep, Step
)
from uclptb.models import Demographics
from uclptb import models as uclptb_models
from tb import models as tb_models


class NextTBStage(ModalPathway):
    display_name = "Next TB Stage"
    slug = "next_tb_stage"

    steps = (Demographics,)


class TBContactTracing(RedirectsToPatientMixin, Pathway):
    display_name = "Contact Tracing"
    slug = "contact_tracing"
    steps = (
        tb_models.EnvironmentalRiskAssessment,
        MultSaveStep(
            model=tb_models.ContactTracing,
            controller_class="ContactTracingFormCtrl"
        ),
    )

class TBScreening(RedirectsToPatientMixin, Pathway):
    display_name = "TB Assessment"
    slug = "tb_assessment"
    steps = (
        Step(
            title="Personal Information",
            model=uclptb_models.Demographics,
            template_url="/templates/personal_information_form.html",
        ),
        Step(
            title="Presentation & History",
            model=uclptb_models.SymptomComplex,
            template_url="/templates/presentation_pathway.html",
            controller_class="TBSymptomsFormCtrl"
        ),
        # Step(
        #     model=tb_models.TBTests,
        # ),
        uclptb_models.PatientConsultation

        # PatientConsultation (in a timeline on the patient detail view)
    )


class TreatmentOutcome(RedirectsToPatientMixin, pathways.Pathway):
    """
    The pathway we use to record the outcome of a course of TB.
    """
    display_name = "TB Treatment Outcome"
    slug         = "tb_treatment_outcome"
    steps = (
        tb_models.TBOutcome,
    )
