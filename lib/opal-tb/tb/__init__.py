"""
Plugin definition for the tb OPAL plugin
"""
from opal.core import plugins

from tb.urls import urlpatterns

class TbPlugin(plugins.OpalPlugin):
    """
    Main entrypoint to expose this plugin to our OPAL application.
    """
    urls = urlpatterns
    javascripts = {
        # Add your javascripts here!
        'opal.controllers': [
            'js/tb/controllers/contact_tracing_form.js',
            'js/tb/controllers/personal_information.js',
            "js/tb/controllers/tb_symptoms_form.js",
            # 'js/tb/app.js',
            # 'js/tb/controllers/larry.js',
            # 'js/tb/services/larry.js',
        ]
    }

    def restricted_teams(self, user):
        """
        Return any restricted teams for particualr users that our
        plugin may define.
        """
        return []

    def list_schemas(self):
        """
        Return any patient list schemas that our plugin may define.
        """
        return {}

    def flows(self):
        """
        Return any custom flows that our plugin may define
        """
        return {}

    def roles(self, user):
        """
        Given a (Django) USER object, return any extra roles defined
        by our plugin.
        """
        return {}


plugins.register(TbPlugin)
