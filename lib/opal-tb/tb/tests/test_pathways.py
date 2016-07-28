from opal.core.test import OpalTestCase
from tb.pathways import TBTreatment, TreatmentOutcome
from opal.models import Episode
from uclptb.models import Treatment



class TestTBTreatment(OpalTestCase):
    def test_save(self):
        patient, episode = self.new_patient_and_episode_please()
        pathway = TBTreatment(patient_id=patient.id, episode_id=episode.id)
        example_data = dict(stage=['Active TB'], treatment=[])
        pathway.save(example_data, self.user)
        reloaded_episode = Episode.objects.get()
        self.assertEqual(reloaded_episode.stage, 'Active TB')


class TestTreatmentOutcome(OpalTestCase):
    def test_save(self):
        patient, episode = self.new_patient_and_episode_please()
        pathway = TreatmentOutcome(
            patient_id=patient.id, episode_id=episode.id
        )
        pathway.save({}, self.user)
        reloaded_episode = Episode.objects.get()
        self.assertEqual(reloaded_episode.stage, 'Discharged')


class TBContactTracingTestCase(OpalTestCase):
    def test_sets_contact_tracing_in_tb_meta(self):
        from tb import pathways
        p, e = self.new_patient_and_episode_please()
        pathway = pathways.TBContactTracing(patient_id=p.id, episode_id=e.id)
        pathway.save({}, self.user)
        self.assertEqual(True, e.tbmeta_set.get().contact_tracing_done)
