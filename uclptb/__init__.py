"""
uclptb - Our OPAL Application
"""
from opal.core import application

class Application(application.OpalApplication):
    schema_module = 'uclptb.schema'
    flow_module   = 'uclptb.flow'
    javascripts   = [
        'js/uclptb/routes.js',
        'js/opal/controllers/discharge.js'
    ]