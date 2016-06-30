from opal.core import episodes


class TBEpisodeStages(object):
    CONTACT_TRACING = "Contact tracing"


class TBEpisode(episodes.EpisodeCategory):
    display_name = "TB"
    detail_template = "detail/tb.html"
    stages = TBEpisodeStages
