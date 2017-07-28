"""
Opal Pathway definitions for the re-usable TB module.
"""
import datetime

from django.db import transaction
from django.conf import settings
from opal.core.pathway import (
    RedirectsToPatientMixin,
    Step,
    PagePathway,
    HelpTextStep
)
from episode_categories import TBEpisodeStages

# TODO Stop importing these like this - it makes us unpluggable
from uclptb import models as uclptb_models
from tb import models as tb_models
from opal import models as opal_models


class RemoveEmptiesMixin(object):
    def save(self, data, user=None, **kwargs):
        for subrecordName, subrecords in data.iteritems():
            for index, subrecord in enumerate(subrecords):
                if not subrecord:
                    data[subrecordName].pop(index)

        return super(RemoveEmptiesMixin, self).save(data, user)

SymptomStep = HelpTextStep(
    model=uclptb_models.SymptomComplex,
    template="pathway/steps/symptom_complex.html",
    step_controller="TbSymptomComplexCrtl",
    multiple=False,
    help_text=""
)


class TBAddTests(PagePathway):
    display_name = "Add Tests"
    slug = "add_tests_pathway"
    icon="fa fa-mail-forward"

    steps = (
        Step(
            model=tb_models.TestResult,
            template="pathway/add_tests.html",
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
            template="pathway/add_results.html",
            controller_class="AddResultsCtrl",
        ),
    )

class TBAddPatient(RedirectsToPatientMixin, PagePathway):
    display_name = "Add Patient"
    slug = "tb_add_patient"
    steps = (
        HelpTextStep(
            model=uclptb_models.ReferralRoute,
            help_text="""
                How was the patient referred
                to the TB clinic?
            """
        ),
        HelpTextStep(
            model=uclptb_models.Demographics,
            help_text="""
                Basic demographic information about this patient.
                (Pulled from other hospital systems where available).
            """
        ),
        HelpTextStep(
            model=tb_models.ContactDetails,
            help_text="""
                Contact details for this patient.
                (Pulled from other hospital systems where available).
            """
        ),
    )

    def save(self, data, user=None, patient=None, episode=None):
        if not patient:
            if "hospital_number" not in data["demographics"][0]:
                if "surname" in data["demographics"][0]:
                    patient = opal_models.Patient.objects.create()

        patient, episode = super(TBAddPatient, self).save(
            data, user=user, patient=patient, episode=episode
        )
        episode.stage = TBEpisodeStages.NEW_REFERRAL
        episode.date_of_admission = datetime.date.today()
        episode.save()

        return patient, episode


class TBContactTracing(RedirectsToPatientMixin, PagePathway):
    display_name = "Contact Tracing"
    slug = "contact_tracing"
    steps = (
        Step(
            model=tb_models.ContactTracing,
            template="pathway/contact_tracing.html"
        ),
    )

    def save(self, data, user=None, **kwargs):
        """
        Set this step as done in TBMeta
        """
        patient, episode = super(TBContactTracing, self).save(data, user=user)
        meta = self.episode.tbmeta_set.get()
        meta.contact_tracing_done = True
        meta.save()
        return patient


class TBAssessment(RedirectsToPatientMixin, PagePathway):
    display_name = "TB Assessment"
    slug = "tb_initial_assessment"
    steps = (
        SymptomStep,
        HelpTextStep(
            model=tb_models.TBHistory,
            template="pathway/steps/tb_history.html",
            help_text="""
                Have they had TB before or contact with someone who has had TB
            """
        ),
        HelpTextStep(
            model=uclptb_models.Treatment,
            template="pathway/steps/drug_history.html",
            display_name="Drug History",
        ),
        HelpTextStep(
            model=tb_models.SocialHistory
        ),
        HelpTextStep(
            model=tb_models.SocialHistory,
            template="pathway/steps/geographic_exposure.html",
            display_name="Geographical Exposure",
            icon="fa fa-plane",
            help_text=" ".join([
                "Any countries with a high prevelance of TB where the",
                "patient has spent more than three months."
            ])
        ),
        HelpTextStep(
            model=uclptb_models.PatientConsultation,
            multiple=False,
            help_text="Summary of assessment, impression and plan."
        )
    )

    def save(self, data, user=None, episode=None, patient=None):
        patient, episode = super(TBAssessment, self).save(
            data, user=user, patient=patient, episode=episode
        )
        episode.stage = TBEpisodeStages.UNDER_INVESTIGATION
        episode.save()
        return patient, episode


class TBContactScreening(RedirectsToPatientMixin, PagePathway):
    display_name = "TB Contact Screening"
    slug = "tb_screening"
    steps = (
        HelpTextStep(
            display_name="Already Traced",
            template="_partials/context_traced.html",
            help_text=""
        ),
        Step(
            model=uclptb_models.SymptomComplex,
            template="pathway/tb_contact_screening.html",
            controller_class="TbSymptomComplexCrtl",
            multiple=True
        ),
    )

    def save(self, data, user=None, patient=None, episode=None):
        next_steps = data.pop("next_steps")[0]
        referral_route = data.pop("referral_route", [{}])[0]
        today_str = datetime.datetime.now().strftime(
            settings.DATE_INPUT_FORMATS[0]
        )

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

        patient = super(TBContactScreening, self).save(
            data, user=user, patient=patient, episode=episode)

        if next_steps["result"] == "discharged":
            episode.discharge_date = datetime.date.today()
            episode.stage = TBEpisodeStages.DISCHARGED
            episode.save()
        return patient, episode


class TBObserveDOT(PagePathway):
    display_name = "Observe DOT"
    slug = "observe_dot"
    icon = "fa fa-eye-slash"

    steps = (
        Step(
            model=tb_models.TestResult,
            template="pathway/observe_dot.html",
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
            template="pathway/dot_history.html",
            controller_class="DOTHistoryCtrl",
        ),
    )


class TBTreatment(RemoveEmptiesMixin, RedirectsToPatientMixin, PagePathway):
    display_name  = "TB Treatment"
    slug          = "tb_treatment"
    template_url = '/templates/pathway/treatment_form_base.html'
    icon = 'fa fa-medkit'
    steps = (
        HelpTextStep(
            model=uclptb_models.Diagnosis,
            controller_class=""
        ),
        Step(
            display_name="Diagnosis & Treatment",
            icon="fa fa-medkit",
            template="pathway/tb_treatment.html",
            controller_class="TBTreatmentCtrl",
        ),
    )

    @transaction.atomic
    def save(self, data, user=None, **kwargs):
        stage = data.pop('stage')[0]
        patient, episode = super(TBTreatment, self).save(data, user=user, **kwargs)
        episode.stage = stage
        episode.save()
        return patient, episode


class TreatmentOutcome(RedirectsToPatientMixin, PagePathway):
    """
    The pathway we use to record the outcome of a course of TB.
    """
    display_name = "TB Treatment Outcome"
    slug         = "tb_treatment_outcome"
    steps = (
        tb_models.TBOutcome,
    )

    def save(self, data, **kwargs):
        patient, episode = super(TreatmentOutcome, self).save(data, **kwargs)
        episode.stage = TBEpisodeStages.DISCHARGED
        episode.discharge_date = datetime.date.today()
        episode.save()
        return patient, episode
