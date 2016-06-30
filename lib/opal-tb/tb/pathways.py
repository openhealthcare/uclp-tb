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
        MultSaveStep(
            model=tb_models.ContactTracing,
            controller_class="ContactTracingFormCtrl"
        ),
    )

class TBScreening(RedirectsToPatientMixin, Pathway):
    display_name = "TB Screening"
    slug = "tb_screening"
    steps = (
        Step(
            title="Personal Information",
            model=uclptb_models.Demographics,
            template_url="/templates/personal_information_form.html",
            controller_class="PersonalInformationCtrl"
        ),
        Step(
            title="Presentation & History",
            model=uclptb_models.SymptomComplex,
            template_url="/templates/presentation_pathway.html",
            controller_class="PersonalInformationCtrl"
        ),
        # # # combine the 2 into one custom step
        # tb_models.EnvironmentalTBRiskFactors,
        # # this needs display logic work
        #
        # tb_models.MedicalTBRiskFactors,
        # # inline check boxes
        #
        # MultSaveStep(model=uclptb_models.SymptomComplex),
        # MultSaveStep(model=uclptb_models.PastMedicalHistory),
        #
        # # combine the 2 into one custom step
        # MultSaveStep(
        #     model=uclptb_models.Investigation,
        #     controller_class="InvestigationFormCtrl"
        # ),
        # Radiology
        Step(
            model=tb_models.TBRadiology,
            title="Tests",
            template_url="/templates/tests_pathway_form.html",
        ),
        uclptb_models.PatientConsultation

        # PatientConsultation (in a timeline on the patient detail view)
    )
