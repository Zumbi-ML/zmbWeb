import about.view as msweb_aview
from tests.util import ZumbiWebBaseTest

"""
Tests for the about app view.
"""

# Functions to exclude from this test
EXCLUDE = []


class TestAboutViews(ZumbiWebBaseTest):
    def test_search_view(self):
        self.run_test_for_all_functions_in_module(msweb_aview, EXCLUDE)
