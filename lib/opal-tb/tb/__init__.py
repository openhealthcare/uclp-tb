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
        'opal.controllers': [
            'js/tb/controllers/tb_treatment.js',
            "js/tb/controllers/tb_symptoms_form.js",
            "js/tb/controllers/tb_type.js",
            "js/tb/controllers/test_results.js",
            "js/tb/directives.js",
        ],
        'opal.services': [
        ]
    }


plugins.register(TbPlugin)
