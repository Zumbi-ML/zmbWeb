# -*- coding: utf-8 -*-

from extract.logic import get_random_abstract
from tests.util import ZumbiWebBaseTest

# from extract.logic import extracted_results

"""
Tests for the extract app callback logic.
"""


class TestExtractLogic(ZumbiWebBaseTest):
    def test_extracted_results(self):
        pass

    def test_get_random_abstract(self):
        ab = get_random_abstract(random_button_n_clicks=0)
        self.assertTrue(ab in [None, ""])
        ab = get_random_abstract(random_button_n_clicks=1)
        self.assertTrue(isinstance(ab, str))
        self.assertGreater(len(ab), 10)
        ab = get_random_abstract(random_button_n_clicks=100)
        self.assertTrue(isinstance(ab, str))
        self.assertGreater(len(ab), 10)
