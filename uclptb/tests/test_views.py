from django.core.urlresolvers import reverse

from opal.core.test import OpalTestCase
from opal.core.subrecords import subrecords


class ViewsTest(OpalTestCase):
    def test_all_modal_templates(self):
        """ This renders all of our modal templates and blows up
            if they fail to render
        """
        for i in subrecords():
            if i.get_form_template():
                url = reverse("{}_modal".format(i.get_api_name()))
                self.assertStatusCode(url, 200)
