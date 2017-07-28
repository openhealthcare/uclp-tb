"""
Defining OPAL PatientLists
"""
from opal import core
from opal.models import Episode

from uclptb import models


class AllPatientsList(core.patient_lists.PatientList):
    display_name = 'All Patients'
    allow_add_patient = False

    schema = [
        models.Demographics,
        models.Diagnosis,
        models.Treatment
    ]

    def get_queryset(self, user):
        return Episode.objects.all()
