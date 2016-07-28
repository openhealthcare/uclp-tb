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
        self.assertEqual(datetime.date.today(), episode.date_of_admission)


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
