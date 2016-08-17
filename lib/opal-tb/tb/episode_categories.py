from opal.core import episodes
from opal.core import metadata

class TBEpisodeStages(metadata.Metadata):

    # contact has been flagged as a potential risk
    NEW_CONTACT = "New Contact"

    # contact has been referred either through contact screening
    # or a direct referral
    NEW_REFERRAL = "New Referral"

    # patient has gone through the initial assessment and tests
    # have probably been sent off
    UNDER_INVESTIGATION = "Under Investigation"

    # patient is undergoing active tb treatment
    ACTIVE_TB_TREATMENT = "Active TB Treatment"

    # patient is undergoing latent tb treatment
    LATENT_TB_TREATMENT = "Latent TB Treatment"

    # patient has been discharged
    DISCHARGED = "Discharged"

    # NTM are Non-tuberculous Mycobacterial Infections
    NTM_TREATMENT = "NTM Treatment"
    stages = [
        NEW_CONTACT,
        NEW_REFERRAL,
        UNDER_INVESTIGATION,
        ACTIVE_TB_TREATMENT,
        LATENT_TB_TREATMENT,
        NTM_TREATMENT,
        DISCHARGED
    ]

    @classmethod
    def to_dict(cls, **kw):
        stages = { i.replace(" ", "_").lower(): i for i in cls.stages}
        return { TBEpisode.get_slug(): dict(stages=stages) }


class TBEpisode(episodes.EpisodeCategory):
    display_name = "TB"
    detail_template = "detail/tb.html"
    stages = TBEpisodeStages.stages
