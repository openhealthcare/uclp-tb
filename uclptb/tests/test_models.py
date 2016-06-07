from opal.core.test import TestCase
from episode_categories import TBEpisode


class EpisodeCategoryTestCase(TestCase):
    def test_default_episode_category(self):
        _, episode = self.new_patient_and_episode_please()
        self.assertEqual(episode.category.__class__, TBEpisode)
