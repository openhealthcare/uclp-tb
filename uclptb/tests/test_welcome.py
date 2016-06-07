from opal.core.test import OpalTestCase
from django.core.urlresolvers import reverse


class TestWelcome(OpalTestCase):
    def setUp(self):
        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )

    def test_render_200(self):
        patient, episode = self.new_patient_and_episode_please()
        url = "templates/welcome.html"
        self.assertContains(url, 200)
