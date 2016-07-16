"""
OPAL Pathway definitions for the re-usable TB module.
"""
from pathway import pathways
from pathway.pathways import (
    ModalPathway, Pathway, RedirectsToPatientMixin, Step
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
        Step(
            model=tb_models.ContactTracing,
            template_url="/templates/contact_tracing.html"
        ),
    )

class TBTreatment(RedirectsToPatientMixin, Pathway):
    display_name  = "TB Treatment"
    slug          = "tb_treatment"
    template_url = '/templates/pathway/treatment_form_base.html'
    steps = (
        # Step(
        #     title="TB Type",
        #     icon="fa fa-tag",
        #     api_name="stage",
        #     template_url="/templates/tb_type.html",
        #     controller_class="TBTypeFormCtrl",
        # ),
        Step(
            title="Diagnosis & Treatment",
            icon="fa fa-medkit",
            template_url="/templates/tb_treatment.html",
            controller_class="TBTreatmentCtrl",
        ),
    )

    def save(self, data, user):
        stage = data.pop('stage')[0]
        episode = self.episode
        patient = super(TBTreatment, self).save(data, user)
        episode.stage = stage
        episode.save()
        return patient


class TBAssessment(RedirectsToPatientMixin, Pathway):
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

    def save(self, data, user):
        patient = super(TreatmentOutcome, self).save(data, user)
        episode = self.episode
        episode.stage = 'Discharged'
        episode.save()
        return patient
