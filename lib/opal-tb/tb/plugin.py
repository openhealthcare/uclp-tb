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
            "js/tb/controllers/tb_add_patient.js",
            "js/tb/controllers/add_tests.js",
            "js/tb/controllers/add_results.js",
            "js/tb/controllers/results_tab.js",
            "js/tb/controllers/observe_dot.js",
            "js/tb/controllers/dot_history.js",
            "js/tb/directives.js",
        ],
        'opal.services': [
            "js/tb/services/test_result_record.js",
            "js/tb/services/treatment_utils.js",
        ]
    }
