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
            "js/tb/controllers/tb_initial_assessment.js",
            "js/tb/controllers/tb_type.js",
            "js/tb/controllers/add_tests.js",
            "js/tb/controllers/add_results.js",
            "js/tb/controllers/results_tab.js",
            "js/tb/directives.js",
        ],
        'opal.services': [
            "js/tb/services/test_result_record.js",
        ]
    }


plugins.register(TbPlugin)
