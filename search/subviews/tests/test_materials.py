# -*- coding: utf-8 -*-

import unittest

import search.subviews.materials as msweb_ssm
from search.subviews.tests.util import common_arg_combos
from tests.util import (
    ZumbiWebBaseTest,
    all_rester_requirements_defined,
)


"""
Tests for the materials subview of search.
"""


class TestSearchMaterialsSubview(ZumbiWebBaseTest):
    @unittest.skipIf(
        not all_rester_requirements_defined, "API access and endpoint not set."
    )
    def test_materials_results_html(self):
        """
        This generally tests everything in the subview since all functions are
        dependent on the single results html.

        Hence we don't need run_test_for_all_functions_in_submodule.
        """
        f = msweb_ssm.materials_results_html
        self.run_test_for_individual_arg_combos(f, common_arg_combos)
