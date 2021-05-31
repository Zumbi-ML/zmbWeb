import journals.view as msweb_jv
from tests.util import ZumbiWebBaseTest

"""
Tests for the journals view.
"""

# Functions to exclude from this test
EXCLUDE = []


class TestJournalsView(ZumbiWebBaseTest):
    def test_journal_views(self):
        self.run_test_for_all_functions_in_module(msweb_jv, EXCLUDE)
