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
    def save(self, data, user=None, patient=None, episode=None):
        for subrecordName, subrecords in data.iteritems():
            for index, subrecord in enumerate(subrecords):
                if not subrecord:
                    data[subrecordName].pop(index)

        return super(RemoveEmptiesMixin, self).save(
            data, user, patient, episode
        )

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
            step_controller="AddTestsCtrl",
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
            step_controller="AddResultsCtrl",
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

    @transaction.atomic
    def save(self, data, user=None, patient=None, episode=None):
        if not patient:
            if "hospital_number" not in data["demographics"][0]:
                if "surname" in data["demographics"][0]:
                    patient = opal_models.Patient.objects.create()

        patient, episode = super(TBAddPatient, self).save(
            data, user=user, patient=patient, episode=episode
        )
        episode.stage = TBEpisodeStages.NEW_REFERRAL
        episode.start = datetime.date.today()
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

    @transaction.atomic
    def save(self, data, user=None, episode=None, patient=None):
        """
        Set this step as done in TBMeta
        """
        patient, episode = super(TBContactTracing, self).save(
            data, user=user, episode=episode, patient=patient
        )
        meta = episode.tbmeta_set.get()
        meta.contact_tracing_done = True
        meta.save()
        return patient, episode


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

    @transaction.atomic
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
            step_controller="TbSymptomComplexCrtl",
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
            step_controller="ObserveDOTCtrl",
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
            step_controller="DOTHistoryCtrl",
        ),
    )


class TBTreatment(RemoveEmptiesMixin, RedirectsToPatientMixin, PagePathway):
    display_name  = "TB Treatment"
    slug          = "tb_treatment"
    icon = 'fa fa-medkit'
    steps = (
        HelpTextStep(
            model=uclptb_models.Diagnosis,
            template="pathway/steps/tb_diagnosis.html",
            step_controller="TBDiagnosis",
            help_text=""""
                What type of TB does this patient have,
                and where is it located?"
            """
        ),
        HelpTextStep(
            display_name="Test Results",
            icon="fa fa-crosshairs",
            template="_partials/results_table.html",
            help_text="A brief summary of the key test results for this patient."
        ),
        HelpTextStep(
            display_name="Current Treatment",
            icon="fa fa-medkit",
            template="partials/current_treatments.html"
        ),
        HelpTextStep(
            display_name="Treatment Plan",
            icon="fa fa-medkit",
            base_template="pathway/steps/treatment_plan_base.html",
            # we use the base template instead
            template="not_used.html",
            step_controller="TBTreatmentCtrl",
        ),
        HelpTextStep(
            model=uclptb_models.PatientConsultation,
            multiple=False,
        )
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
