from opal.core.test import OpalTestCase
from uclptb.episode_categories import TBEpisode


class EpisodeCategoryTestCase(OpalTestCase):
    def test_default_episode_category(self):
        _, episode = self.new_patient_and_episode_please()
        self.assertEqual(episode.category.__class__, TBEpisode)
