"""
Unittests for uclptb.patient_lists
"""
from opal.core.test import OpalTestCase

from uclptb import patient_lists

class PatientListTestCase(OpalTestCase):
    def test_queryset(self):
        all_patients = patient_lists.AllPatientsList()
        self.assertEqual(0, all_patients.get_queryset().count())
        patient, episode = self.new_patient_and_episode_please()
        self.assertEqual(1, all_patients.get_queryset().count())
