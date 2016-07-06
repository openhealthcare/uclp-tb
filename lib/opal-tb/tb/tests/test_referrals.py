"""
Unittests for the tb.referrals module
"""
from opal.core.test import OpalTestCase

from tb import referrals

class TBReferralTestCase(OpalTestCase):

    def test_success_link(self):
        p, e = self.new_patient_and_episode_please()
        route = referrals.TBReferral()
        link = route.get_success_link(e)
        self.assertEqual('/#/patient/{0}'.format(p.id), link)

    def test_post_create(self):
        p, e = self.new_patient_and_episode_please()
        route = referrals.TBReferral()
        self.assertEqual(None, e.stage)
        route.post_create(e, None)
        self.assertEqual("Under Investigation", e.stage)


class TestReferralViews(OpalTestCase):
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
        self.assertStatusCode(url, 200)
