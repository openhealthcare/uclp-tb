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

class TBTreatment(RedirectsToPatientMixin, Pathway):
    display_name = "TB Treatment"
    slug = "tb_treatment"
    steps = (
        Step(
            title="TB Type",
            icon="fa fa-tag",
            api_name="stage",
            template_url="/templates/tb_type.html",
            controller_class="TBTypeFormCtrl",
        ),
        Step(
            title="Treatment",
            icon="fa fa-medkit",
            template_url="/templates/tb_treatment.html",
            controller_class="BloodCulturePathwayCtrl",
        )
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
