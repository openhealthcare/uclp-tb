import datetime
from opal.core.test import OpalTestCase
from opal.core import subrecords, exceptions
from tb.models import ContactTracing


class ContactTracingTestCase(OpalTestCase):
    def setUp(self):
        self.patient, self.episode = self.new_patient_and_episode_please()
        self.other_patient, self.other_episode = self.new_patient_and_episode_please()
        self.other_patient.demographics_set.update(
            first_name="other",
            surname="patient"
        )
        self.other_patient.contactdetails_set.update(
            address_line1="1 London"
        )

    def get_test_dict(self):
        return {
            "address_line1": "2 London",
            "address_line2":  None,
            "birth_place": "",
            "birth_place_fk_id": None,
            "birth_place_ft": "",
            "city": "",
            "consistency_token": "",
            "contact_episode_id": 16,
            "county": None,
            "created": None,
            "created_by_id": None,
            "date_of_birth": None,
            "date_of_death": None,
            "death_indicator": False,
            "episode_id": 12,
            "ethnicity": "",
            "ethnicity_fk_id": None,
            "ethnicity_ft": "",
            "first_name": "Wade",
            "gp_practice_code": None,
            "hospital_number": "23423232332",
            "id": 5,
            "marital_status": "",
            "marital_status_fk_id": None,
            "marital_status_ft": "",
            "middle_name": None,
            "nhs_number": None,
            "patient_id": 11,
            "post_code": None,
            "religion": None,
            "sex": "",
            "sex_fk_id": None,
            "sex_ft": "",
            "stage": "Contact tracing",
            "surname": "Wilson",
            "tel1": None,
            "tel2": None,
            "title": "Mr",
            "title_fk_id": 2,
            "title_ft": "",
            "updated": None,
            "updated_by_id": None,
        }

    def test_build_field_schema(self):
        """ the python dict should be a sub set of
            what we are getting back through schema
        """
        result = ContactTracing.build_field_schema()
        models = set(i["model"] for i in result)
        self.assertEqual(
            models, set(["Demographics", "ContactDetails", "ContactTracing"])
        )
        fields = set(i["name"] for i in result if not i["name"] == "id")
        example_fields = set(self.get_test_dict().keys())
        self.assertFalse(fields - example_fields)

    def test_build_field_schema_to_dict_equivalence(self):
        """ because we build the schema independently of the
            serialisation, so there are no field in to dict
            that are not in schema
        """

        new_contact_tracing = ContactTracing.objects.create(
            episode=self.episode,
            contact_episode=self.other_episode
        )

        found_keys = set(new_contact_tracing.to_dict(self.user).keys())
        expected_keys = set(
            i["name"] for i in ContactTracing.build_field_schema()
        )
        no_difference = expected_keys - found_keys
        self.assertFalse(no_difference)


    def test_update_contact_tracing(self):
        """
        we don't allow updates for contact tracing, make sure
        any update sent won't blow up or change anything
        """
        ContactDetails = subrecords.get_subrecord_from_model_name('ContactDetails')
        Demographics = subrecords.get_subrecord_from_model_name('Demographics')

        new_contact_tracing = ContactTracing.objects.create(
            episode=self.episode,
            contact_episode=self.other_episode
        )

        example_update_dict = self.get_test_dict()
        example_update_dict["id"] = new_contact_tracing.id

        # so we expcect it to update the demographics
        # and contact details the new values
        new_contact_tracing.update_from_dict(example_update_dict, self.user)
        self.assertEqual(ContactTracing.objects.count(), 1)
        self.assertEqual(Demographics.objects.count(), 2)
        self.assertEqual(ContactDetails.objects.count(), 2)
        demographics = new_contact_tracing.contact_episode.patient.demographics_set.first()
        self.assertEqual(
            demographics.first_name,
            self.other_patient.demographics_set.first().first_name
        )

        contact_details = new_contact_tracing.contact_episode.patient.contactdetails_set.first()
        self.assertEqual(
            contact_details.address_line1,
            self.other_patient.contactdetails_set.first().address_line1
        )

    def test_create_new_contact_tracing(self):
        ContactDetails = subrecords.get_subrecord_from_model_name('ContactDetails')
        Demographics = subrecords.get_subrecord_from_model_name('Demographics')

        new_contact_tracing = ContactTracing(episode=self.episode)
        example_update_dict = self.get_test_dict()
        new_contact_tracing.update_from_dict(example_update_dict, self.user)
        self.assertEqual(ContactTracing.objects.count(), 1)
        self.assertEqual(Demographics.objects.count(), 3)
        self.assertEqual(ContactDetails.objects.count(), 3)
        demographics = new_contact_tracing.contact_episode.patient.demographics_set.first()
        self.assertEqual(
            demographics.first_name,
            example_update_dict["first_name"]
        )

        contact_details = new_contact_tracing.contact_episode.patient.contactdetails_set.first()
        self.assertEqual(
            contact_details.address_line1,
            example_update_dict["address_line1"]
        )

    def test_to_dict(self):
        new_contact_tracing = ContactTracing.objects.create(
            episode=self.episode,
            contact_episode=self.other_episode
        )
        distant_past = datetime.datetime.now() - datetime.timedelta(54)
        new_contact_tracing.episode.patient.demographics_set.update(
            created=distant_past, updated=distant_past
        )
        new_contact_tracing.episode.patient.contactdetails_set.update(
            created=distant_past, updated=distant_past
        )

        recent_past = datetime.datetime.now() - datetime.timedelta(1)
        new_contact_tracing.created = recent_past
        new_contact_tracing.updated = recent_past

        result = new_contact_tracing.to_dict(self.user)
        self.assertEqual(result["first_name"], "other")
        self.assertEqual(result["id"], new_contact_tracing.id)
        self.assertEqual(result["created"], new_contact_tracing.created)
        self.assertEqual(result["updated"], new_contact_tracing.updated)
        self.assertEqual(result["address_line1"], "1 London")
