from opal.core.test import OpalTestCase
from tb.pathways import TBTreatment, TreatmentOutcome
from opal.models import Episode
from uclptb.models import Treatment



class TestTBTreatment(OpalTestCase):
    def test_save(self):
        patient, episode = self.new_patient_and_episode_please()
        pathway = TBTreatment(patient_id=patient.id, episode_id=episode.id)
        Treatment.objects.create(episode=episode, drug="Aspirin")

        example_data = dict(stage=['Active TB'], treatment=[{"drug": "Paracetomol"}])
        pathway.save(example_data, self.user)
        reloaded_episode = Episode.objects.get()
        self.assertEqual(reloaded_episode.stage, 'Active TB')
        self.assertEqual(reloaded_episode.treatment_set.get().drug, "Paracetomol")


class TestTreatmentOutcome(OpalTestCase):
    def test_save(self):
        patient, episode = self.new_patient_and_episode_please()
        pathway = TreatmentOutcome(
            patient_id=patient.id, episode_id=episode.id
        )
        pathway.save({}, self.user)
        reloaded_episode = Episode.objects.get()
        self.assertEqual(reloaded_episode.stage, 'Discharged')
