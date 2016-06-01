"""
tbshowcase - Our OPAL Application
"""
from opal.core import application

class Application(application.OpalApplication):
    schema_module = 'tbshowcase.schema'
    flow_module   = 'tbshowcase.flow'
    javascripts   = [
        'js/tbshowcase/routes.js',
        'js/opal/controllers/discharge.js'
    ]