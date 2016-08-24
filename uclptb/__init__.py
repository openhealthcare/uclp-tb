"""
uclptb - Our OPAL Application
"""
from opal.core import application

class Application(application.OpalApplication):
    schema_module = 'uclptb.schema'
    flow_module   = 'uclptb.flow'
    javascripts   = [
        'js/uclptb/routes.js',
        'js/opal/controllers/discharge.js',
        'js/uclptb/services/records/treatment_record.js',
        'js/uclptb/controllers/treatment_modal_form.js',
        'js/uclptb/controllers/current_treatment_panel.js',
    ]
    default_episode_category = 'TB'
    styles = [
        'css/tb.css'
    ]
    menuitems = [
        dict(
            href='/pathway/#/tb_add_patient', display='Add Patient', icon='fa fa-plus',
            activepattern='/referrals/#/ucl_ptb'),
    ]
