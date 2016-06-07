from opal.core.test import OpalTestCase


class TestReferral(OpalTestCase):
    def setUp(self):
        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )

    def test_route_200(self):
        # hard coding the url because its
        # hard coded in the navigation bar
        url = '/referrals/#/ucl_ptb'
        self.assertContains(url, 200)
