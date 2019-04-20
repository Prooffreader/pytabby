#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Note that all formatting functions require a config that has gone through normalizer.normalize()

Only regression tests are used for these, because it's string output.
Just don't forget to replace data files if input file changes.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from copy import deepcopy

import pytest

import tabbedshellmenus.formatting as formatting
import tabbedshellmenus.normalizer as normalizer


@pytest.mark.regression
@pytest.mark.run(order=2)
def test_regress__format_headers(data_regression, config_multiple):
    """Only multiple-type schema has headers; no need to normalize"""
    tab_num = 1  # minimum non-first ordinal of a multiple tab layout
    c = deepcopy(config_multiple)
    result = formatting._format_headers(c["tabs"], tab_num, 80)
    data = {"data": result}
    data_regression.check(data)


@pytest.mark.regression
@pytest.mark.run(order=3)
def test_regress__format_menu(data_regression, config_all_with_id):
    """Normalize first"""
    config, id_ = config_all_with_id
    c = deepcopy(config)
    if id_.find("multiple") != -1:
        tab_num = 1
    else:
        tab_num = 0
    c = normalizer.normalize(c)
    result = formatting.format_menu(c, tab_num, 80).split("\n")
    data = {"data": result}
    data_regression.check(data)


@pytest.mark.regression
@pytest.mark.run(order=3)
class TestEdgeCases:
    """Edge cases to get 100% coverage. Will use only one config each"""

    def test_regress_tab_header_description_none(self, data_regression, config_multiple):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_multiple)
        c["tabs"][0]["tab_header_description"] = None
        result = formatting._format_headers(c["tabs"], 0, 80)
        data = {"data": result}
        data_regression.check(data)

    def test_regress_missing_tab_header_description(self, data_regression, config_multiple):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_multiple)
        if "tab_header_description" in c["tabs"][0].keys():
            del c["tabs"][0]["tab_header_description"]
        result = formatting._format_headers(c["tabs"], 0, 80)
        data = {"data": result}
        data_regression.check(data)

    def test_many_tabs_with_long_headers(self, data_regression, config_multiple):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_multiple)
        c["tabs"][0]["tab_header_input"] = "abcdefghij"
        c["tabs"][0]["tab_header_description"] = "klmnopqrstuvwxyz"
        c["tabs"][1]["tab_header_input"] = "abcdefghijx"
        c["tabs"][1]["tab_header_description"] = "klmnopqrstuvwxyzx"
        c["tabs"].append(c["tabs"][0])
        c["tabs"][-1]["tab_header_input"] = "xabcdefghij"
        c["tabs"][-1]["tab_header_description"] = "xklmnopqrstuvwxyz"
        result = formatting._format_headers(c["tabs"], 0, 80)
        data = {"data": result}
        data_regression.check(data)
