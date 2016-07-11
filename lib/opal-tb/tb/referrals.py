"""
Referral routes for uclp tb
"""
from referral import ReferralRoute


class TBReferral(ReferralRoute):
    name = 'UCLP TB'
    description = 'UCLP - TB'

    def get_success_link(self, episode):
        return '/#/patient/%s' % episode.patient.id

    def post_create(self, episode, user):
        episode.stage = 'Under Investigation'
        import ipdb; ipdb.set_trace()
        episode.save()
