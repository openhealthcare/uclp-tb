"""
Opal Pathway definitions for the re-usable TB module.
"""
import datetime

from django.db import transaction
from django.conf import settings
from pathway import pathways
from pathway.pathways import (
    RedirectsToPatientMixin,
    Step,
    PagePathway
)
from episode_categories import TBEpisodeStages

# TODO Stop importing these like this - it makes us unpluggable
from uclptb import models as uclptb_models
from tb import models as tb_models
from opal import models as opal_models


class RemoveEmptiesMixin(object):
    def save(self, data, user):
        for subrecordName, subrecords in data.iteritems():
            for index, subrecord in enumerate(subrecords):
                if not subrecord:
                    data[subrecordName].pop(index)

        return super(RemoveEmptiesMixin, self).save(data, user)


class TBAddTests(PagePathway):
    display_name = "Add Tests"
    slug = "add_tests_pathway"
    icon="fa fa-mail-forward"

    steps = (
        Step(
            model=tb_models.TestResult,
            template_url="/templates/pathway/add_tests.html",
            controller_class="AddTestsCtrl",
        ),
    )

class TBAddResults(PagePathway):
    display_name = "Add Results"
    slug = "add_results_pathway"
    icon="fa fa-reply"

    steps = (
        Step(
            model=tb_models.TestResult,
            template_url="/templates/pathway/add_results.html",
            controller_class="AddResultsCtrl",
        ),
    )

class TBAddPatient(RedirectsToPatientMixin, PagePathway):
    display_name = "Add Patient"
    slug = "tb_add_patient"
    template_url = '/templates/pathway/treatment_form_base.html'
    steps = (
        Step(
            title="Add Patient",
            icon="fa fa-user",
            template_url="/templates/pathway/add_patient_form.html",
            controller_class="TBAddPatientCtrl"
        ),
    )

    def save(self, data, user):
        if not self.patient:
            if "hospital_number" not in data["demographics"][0]:
                if "surname" in data["demographics"][0]:
                    self.patient_id = opal_models.Patient.objects.create().id

        patient = super(TBAddPatient, self).save(data, user)
        episode = patient.episode_set.first()
        episode.stage = TBEpisodeStages.NEW_REFERRAL
        episode.date_of_admission = datetime.date.today()
        episode.save()
        return patient


class TBContactTracing(RedirectsToPatientMixin, PagePathway):
    display_name = "Contact Tracing"
    slug = "contact_tracing"
    steps = (
        Step(
            model=tb_models.ContactTracing,
            template_url="/templates/pathway/contact_tracing.html"
        ),
    )

    def save(self, data, user):
        """
        Set this step as done in TBMeta
        """
        patient = super(TBContactTracing, self).save(data, user)
        meta = self.episode.tbmeta_set.get()
        meta.contact_tracing_done = True
        meta.save()
        return patient


class TBAssessment(RedirectsToPatientMixin, PagePathway):
    display_name = "TB Assessment"
    template_url = '/templates/pathway/treatment_form_base.html'
    slug = "tb_initial_assessment"
    steps = (
        Step(
            title="Presentation & History",
            model=uclptb_models.SymptomComplex,
            template_url="/templates/pathway/initial_assessment.html",
            controller_class="TBInitialAssessmentCtrl"
        ),
    )

    def save(self, data, user):
        patient = super(TBAssessment, self).save(data, user)
        episode = self.episode
        episode.stage = TBEpisodeStages.UNDER_INVESTIGATION
        episode.save()
        return patient


class TBContactScreening(RedirectsToPatientMixin, PagePathway):
    display_name = "TB Contact Screening"
    template_url = '/templates/pathway/treatment_form_base.html'
    slug = "tb_screening"
    steps = (
        Step(
            title="Contact Screening",
            model=uclptb_models.SymptomComplex,
            template_url="/templates/pathway/tb_contact_screening.html",
            controller_class="TBInitialAssessmentCtrl"
        ),
    )

    def save(self, data, user):
        next_steps = data.pop("next_steps")[0]
        referral_route = data.pop("referral_route", [{}])[0]
        today_str = datetime.datetime.now().strftime(
            settings.DATE_INPUT_FORMATS[0]
        )
        episode = self.episode

        if next_steps["result"] == "referred":
            referral_route["internal"] = True
            referral_route["date_of_referral"] = today_str
            referral_route["referral_organisation"] = "TB Service"

            if user.first_name and user.last_name:
                referral_route["referral_name"] = "{0} {1}".format(
                    user.first_name[0], user.last_name
                )

            data["referral_route"] = [referral_route]

            episode.stage = TBEpisodeStages.NEW_REFERRAL
            episode.save()

        patient = super(TBContactScreening, self).save(data, user)

        if next_steps["result"] == "discharged":
            episode.discharge_date = datetime.date.today()
            episode.stage = TBEpisodeStages.DISCHARGED
            episode.save()
        return patient


class TBObserveDOT(PagePathway):
    display_name = "Observe DOT"
    slug = "observe_dot"
    icon = "fa fa-eye-slash"

    steps = (
        Step(
            model=tb_models.TestResult,
            template_url="/templates/pathway/observe_dot.html",
            controller_class="ObserveDOTCtrl",
        ),
    )


class TBDOTHistory(PagePathway):
    display_name = "DOT History"
    slug = "dot_history"
    icon = "fa fa-history"

    steps = (
        Step(
            model=tb_models.TestResult,
            template_url="/templates/pathway/dot_history.html",
            controller_class="DOTHistoryCtrl",
        ),
    )


class TBTreatment(RemoveEmptiesMixin, RedirectsToPatientMixin, PagePathway):
    display_name  = "TB Treatment"
    slug          = "tb_treatment"
    template_url = '/templates/pathway/treatment_form_base.html'
    icon = 'fa fa-medkit'
    steps = (
        Step(
            title="Diagnosis & Treatment",
            icon="fa fa-medkit",
            template_url="/templates/pathway/tb_treatment.html",
            controller_class="TBTreatmentCtrl",
        ),
    )

    @transaction.atomic
    def save(self, data, user):
        stage = data.pop('stage')[0]
        episode = self.episode
        patient = super(TBTreatment, self).save(data, user)
        episode.stage = stage
        episode.save()
        return patient


class TreatmentOutcome(RedirectsToPatientMixin, pathways.PagePathway):
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
        episode.stage = TBEpisodeStages.DISCHARGED
        episode.discharge_date = datetime.date.today()
        episode.save()
        return patient
