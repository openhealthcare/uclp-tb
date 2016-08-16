"""
Unittests for the tb.pathways module
"""
import datetime

from opal.core.test import OpalTestCase
from opal.models import Episode
from uclptb.models import Treatment

from tb import pathways

class TestTBAddPatientTestCase(OpalTestCase):
    def test_save_sets_episode_start_date(self):
        pathway = pathways.TBAddPatient(patient_id=None, episode_id=None)
        patient = pathway.save({'demographics': [{'hospital_number': '1234'}]}, self.user)
        episode = patient.episode_set.first()
        self.assertEqual(datetime.date.today(), episode.start)


class TestTBTreatment(OpalTestCase):
    def test_save(self):
        patient, episode = self.new_patient_and_episode_please()
        pathway = pathways.TBTreatment(patient_id=patient.id, episode_id=episode.id)
        example_data = dict(stage=['Active TB'], treatment=[])
        pathway.save(example_data, self.user)
        reloaded_episode = Episode.objects.get()
        self.assertEqual(reloaded_episode.stage, 'Active TB')


class TestTreatmentOutcome(OpalTestCase):
    def test_save(self):
        patient, episode = self.new_patient_and_episode_please()
        pathway = pathways.TreatmentOutcome(
            patient_id=patient.id, episode_id=episode.id
        )
        pathway.save({}, self.user)
        reloaded_episode = Episode.objects.get()
        self.assertEqual(reloaded_episode.stage, 'Discharged')

class TestContactScreening(OpalTestCase):
    def test_discharge(self):
        patient, episode = self.new_patient_and_episode_please()
        episode.stage = "Contact Tracing"
        pathway = pathways.TBContactScreening(
            patient_id=patient.id, episode_id=episode.id
        )
        data = dict(next_steps=[dict(result="discharged")])
        pathway.save(data, self.user)
        reloaded_episode = Episode.objects.get()
        self.assertEqual(
            reloaded_episode.discharge_date, datetime.date.today()
        )

    def test_referral(self):
        patient, episode = self.new_patient_and_episode_please()
        self.user.first_name = "James"
        self.user.surname = "Bond"
        self.user.save()
        episode.stage = "Contact Tracing"
        pathway = pathways.TBContactScreening(
            patient_id=patient.id, episode_id=episode.id
        )
        data = dict(next_steps=[dict(result="referred")])
        pathway.save(data, self.user)
        reloaded_episode = Episode.objects.get()
        referral = episode.referralroute_set.get()
        self.assertEqual(referral.date_of_referral, datetime.date.today())
        self.assertTrue(referral.internal)
        self.assertEqual(referral.referral_organisation, "TB Service")


class TBContactTracingTestCase(OpalTestCase):
    def test_sets_contact_tracing_in_tb_meta(self):
        from tb import pathways
        p, e = self.new_patient_and_episode_please()
        pathway = pathways.TBContactTracing(patient_id=p.id, episode_id=e.id)
        pathway.save({}, self.user)
        self.assertEqual(True, e.tbmeta_set.get().contact_tracing_done)

    def test_save_sets_episode_end_date(self):
        patient, episode = self.new_patient_and_episode_please()
        pathway = pathways.TreatmentOutcome(
            patient_id=patient.id, episode_id=episode.id
        )
        patient = pathway.save({}, self.user)
        episode = patient.episode_set.first()
        self.assertEqual(datetime.date.today(), episode.end)
