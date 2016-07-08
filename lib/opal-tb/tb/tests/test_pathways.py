from opal.core.test import OpalTestCase
from tb.pathways import TBTreatment
from opal.models import Episode



class TestTBTreatment(OpalTestCase):
    def test_save(self):
        patient, episode = self.new_patient_and_episode_please()
        pathway = TBTreatment(patient_id=patient.id, episode_id=episode.id)
        example_data = dict(stage=['Active TB'])
        pathway.save(example_data, self.user)
        reloaded_episode = Episode.objects.get()
        self.assertEqual(reloaded_episode.stage, 'Active TB')
