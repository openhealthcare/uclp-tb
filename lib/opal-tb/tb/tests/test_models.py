"""
Unittests for the tb.models module
"""
import datetime

from opal import models
from opal.core import subrecords
from opal.core.test import OpalTestCase

from tb.models import ContactTracing, ContactTraced


class ContactTestCase(OpalTestCase):
    def setUp(self):
        super(ContactTestCase, self).setUp()
        self.patient, self.episode = self.new_patient_and_episode_please()
        self.other_patient, self.other_episode = self.new_patient_and_episode_please()
        self.other_patient.demographics_set.update(
            first_name="other",
            surname="patient"
        )

    def get_test_dict(self):
        return {
            "address": "2 London",
            "birth_place": "",
            "birth_place_fk_id": None,
            "birth_place_ft": "",
            "consistency_token": "",
            "contact_traced_id": 16,
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
            "post_code": "sw13 0BK",
            "religion": None,
            "relationship_to_index": "Mother",
            "reason_at_risk": "Shared household",
            "sex": "",
            "sex_fk_id": None,
            "sex_ft": "",
            "stage": "Contact tracing",
            "surname": "Wilson",
            "symptomatic": True,
            "telephone": "0208 878 5603",
            "title": "Mr",
            "title_fk_id": 2,
            "title_ft": "",
            "updated": None,
            "updated_by_id": None,
        }



class ContactTracedTestCase(ContactTestCase):
    def test_to_dict(self):
        contact_traced = ContactTraced.objects.create(episode=self.other_episode)
        ContactTracing.objects.create(
            episode=self.episode, contact_traced=contact_traced, relationship_to_index="Mother"
        )
        result = contact_traced.to_dict(self.user)
        self.assertEqual(result["contact_tracing"][0]["episode"]["id"], 1)
        self.assertEqual(result["contact_tracing"][0]["contact_tracing"]["relationship_to_index"], "Mother")


class ContactTracingTestCase(ContactTestCase):

    def test_build_field_schema(self):
        """ the python dict should be a sub set of
            what we are getting back through schema
        """
        result = ContactTracing.build_field_schema()
        models = set(i["model"] for i in result)
        self.assertEqual(
            models, set(["Demographics", "ContactTracing"])
        )
        fields = set(i["name"] for i in result if not i["name"] == "id")
        example_fields = set(self.get_test_dict().keys())
        self.assertFalse(fields - example_fields)

    def test_build_field_schema_to_dict_equivalence(self):
        """ because we build the schema independently of the
            serialisation, so there are no field in to dict
            that are not in schema
        """
        contact_traced = ContactTraced.objects.create(episode=self.other_episode)


        new_contact_tracing = ContactTracing.objects.create(
            episode=self.episode,
            contact_traced=contact_traced
        )

        found_keys = set(new_contact_tracing.to_dict(self.user).keys())
        expected_keys = set(
            i["name"] for i in ContactTracing.build_field_schema()
        )
        no_difference = expected_keys - found_keys
        self.assertFalse(no_difference)

    def test_create_tb_episode_sets_date(self):
        episode = ContactTracing().create_tb_episode(models.Patient.objects.create())
        self.assertEqual(datetime.date.today(), episode.start)

    def test_update_contact_tracing(self):
        """
        we don't allow updates for contact tracing, make sure
        any update sent won't blow up or change anything
        """
        Demographics = subrecords.get_subrecord_from_model_name('Demographics')

        contact_traced = ContactTraced.objects.create(episode=self.other_episode)

        new_contact_tracing = ContactTracing.objects.create(
            episode=self.episode,
            contact_traced=contact_traced
        )

        example_update_dict = self.get_test_dict()
        example_update_dict["id"] = new_contact_tracing.id

        # so we expcect it to update the demographics
        # and contact details the new values
        new_contact_tracing.update_from_dict(example_update_dict, self.user)
        self.assertEqual(ContactTracing.objects.count(), 1)
        self.assertEqual(Demographics.objects.count(), 2)
        demographics = new_contact_tracing.contact_traced.episode.patient.demographics_set.first()
        self.assertEqual(
            demographics.first_name,
            self.other_patient.demographics_set.first().first_name
        )

        referral_route = new_contact_tracing.contact_traced.episode.referralroute_set.first()
        self.assertEqual(referral_route.referral_type, '')


    def test_create_new_contact_tracing(self):
        Demographics = subrecords.get_subrecord_from_model_name('Demographics')

        new_contact_tracing = ContactTracing(episode=self.episode)
        example_update_dict = self.get_test_dict()
        self.user.first_name = "Indiana"
        self.user.last_name = "Jones"
        self.user.save()
        new_contact_tracing.update_from_dict(example_update_dict, self.user)
        self.assertEqual(ContactTracing.objects.count(), 1)
        self.assertEqual(Demographics.objects.count(), 3)
        demographics = new_contact_tracing.contact_traced.episode.patient.demographics_set.first()
        self.assertEqual(
            demographics.first_name,
            example_update_dict["first_name"]
        )

        address = new_contact_tracing.contact_traced.address
        self.assertEqual(
            address,
            example_update_dict["address"]
        )

        self.assertTrue(new_contact_tracing.contact_traced.symptomatic)

        # update dict alters the dictionary, so refresh
        example_update_dict = self.get_test_dict()

        self.assertEqual(
            new_contact_tracing.reason_at_risk, example_update_dict["reason_at_risk"]
        )
        self.assertEqual(
            new_contact_tracing.relationship_to_index,
            example_update_dict["relationship_to_index"]
        )
        referral_route = new_contact_tracing.contact_traced.episode.referralroute_set.first()
        self.assertEqual(referral_route.referral_type, "TB contact tracing")
        self.assertEqual(referral_route.referral_name, "I Jones")
        self.assertEqual(
            referral_route.date_of_referral, datetime.date.today()
        )
        self.assertTrue(referral_route.internal)
        self.assertTrue(
            referral_route.referral_organisation, "TB Clinic"
        )

        # contact traced should be updated with address, telephone number and symptomatic

    def test_to_dict(self):
        contact_traced = ContactTraced.objects.create(episode=self.other_episode)
        new_contact_tracing = ContactTracing.objects.create(
            episode=self.episode,
            contact_traced=contact_traced
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
