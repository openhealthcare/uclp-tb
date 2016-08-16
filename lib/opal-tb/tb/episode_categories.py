from opal.core import episodes
from opal.core import metadata
from opal.utils import camelcase_to_underscore


class TBEpisodeStages(metadata.Metadata):

    # contact has been flagged as a potential risk
    CONTACT_TRACING = "Contact Tracing"

    # contact has been spoken to and run throught the
    # contact screening pathway
    CONTACT_SCREENING = "Contact Screening"

    # contact is has been through either contact screening
    # or has been referred and is waiting for an appointment
    AWAITING_APPOINTMENT = "Awaiting Appointment"

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
    TNM_TREATMENT = "NTM Treatment"
    stages = [
        CONTACT_TRACING,
        CONTACT_SCREENING,
        AWAITING_APPOINTMENT,
        UNDER_INVESTIGATION,
        ACTIVE_TB_TREATMENT,
        LATENT_TB_TREATMENT,
        DISCHARGED
    ]

    @classmethod
    def to_dict(cls, **kw):
        stages = {camelcase_to_underscore(i): i for i in cls.stages}
        return { TBEpisode.get_slug(): dict(stages=stages) }


class TBEpisode(episodes.EpisodeCategory):
    display_name = "TB"
    detail_template = "detail/tb.html"
    stages = TBEpisodeStages.stages
