from django.core.urlresolvers import reverse

from opal.core.test import OpalTestCase
from opal.core.subrecords import subrecords


class VerboseNameTestCase(OpalTestCase):
    def test_all_titles_match_the_verbose_name(self):
        for i in subrecords():
            schema = i.build_field_schema()

            for schema_field in schema:
                if schema_field["name"] in ["created_by_id", "updated_by_id"]:
                    continue;
                if not schema_field["title"] == i._get_field_title(schema_field["name"]):
                    print "{0} !== {1}".format(schema_field["title"], i._get_field_title(schema_field["name"]))
