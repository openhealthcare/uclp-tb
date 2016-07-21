"""
OPAL Pathway definitions for the re-usable TB module.
"""
from django.db import transaction
from pathway import pathways
from pathway.pathways import (
    Pathway, RedirectsToPatientMixin, Step, delete_others, ModalPathway
)
from uclptb import models as uclptb_models
from tb import models as tb_models

class TBOrderTest(ModalPathway):
    display_name = "Add Tests"
    slug = "tests_ordered_pathway"
    template_url = "/templates/test_results_pathway_base.html"
    icon="fa fa-mail-forward"

    steps = (
        Step(
            model=tb_models.TestResult,
            template_url="/templates/tests_ordered.html",
            controller_class="OrderedTestsCtrl",
        ),
    )

class TBResultsReceived(ModalPathway):
    display_name = "Add Results"
    slug = "results_received_pathway"
    template_url = "/templates/test_results_pathway_base.html"
    icon="fa fa-reply"

    steps = (
        Step(
            model=tb_models.TestResult,
            template_url="/templates/tests_results_received.html",
            controller_class="ResultsReceivedCtrl",
        ),
    )

class TBAddPatient(RedirectsToPatientMixin, Pathway):
    display_name = "Add Patient"
    slug = "tb_add_patient"
    template_url = '/templates/pathway/treatment_form_base.html'
    steps = (
        Step(
            title="Add Patient",
            icon="fa fa-user",
            template_url="/templates/pathway/add_patient_form.html"
        ),
    )

    def save(self, data, user):
        patient = super(TBAddPatient, self).save(data, user)
        episode = patient.episode_set.first()
        episode.stage = 'Under Investigation'
        episode.save()
        return patient


class TBContactTracing(RedirectsToPatientMixin, Pathway):
    display_name = "Contact Tracing"
    slug = "contact_tracing"
    steps = (
        Step(
            model=tb_models.ContactTracing,
            template_url="/templates/contact_tracing.html"
        ),
    )

class TBAssessment(RedirectsToPatientMixin, Pathway):
    display_name = "TB Assessment"
    template_url = '/templates/pathway/treatment_form_base.html'
    slug = "tb_assessment"
    steps = (
        Step(
            title="Presentation & History",
            model=uclptb_models.SymptomComplex,
            template_url="/templates/pathway/initial_assessment.html",
            controller_class="TBSymptomsFormCtrl"
        ),
    )


class TBTreatment(RedirectsToPatientMixin, Pathway):
    display_name  = "TB Treatment"
    slug          = "tb_treatment"
    template_url = '/templates/pathway/treatment_form_base.html'
    steps = (
        Step(
            title="Diagnosis & Treatment",
            icon="fa fa-medkit",
            template_url="/templates/tb_treatment.html",
            controller_class="TBTreatmentCtrl",
        ),
    )

    @transaction.atomic
    def save(self, data, user):
        stage = data.pop('stage')[0]
        episode = self.episode
        # delete_others(data, uclptb_models.Treatment, patient=self.patient, episode=self.episode)
        patient = super(TBTreatment, self).save(data, user)
        episode.stage = stage
        episode.save()
        return patient


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
