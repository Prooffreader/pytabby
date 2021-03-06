#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests pytabby.normalizer.py"""

# pylama: ignore=D102
# pylint: disable=C0116,C0330,W0212,C0103

from copy import deepcopy

import pytest

import pytabby.normalizer as normalizer

@pytest.mark.function
@pytest.mark.run(order=1)
def test__add_tabs_key_if_needed_multiple(config_all_with_id):
    """Tests function

    Function should not change a multiple or single_with_key schema type
    but should change single_without_key
    """
    conf, id_ = config_all_with_id
    c = deepcopy(conf)
    cprime = normalizer._add_tabs_key_if_needed(deepcopy(c))
    if id_.find("without") == -1:
        if c != cprime:
            raise AssertionError
    else:
        if c == cprime:
            raise AssertionError


@pytest.mark.integration
@pytest.mark.run(order=2)
class TestCaseSensitiveOrInsensitive:
    """Performs tests that do not depend on case insensitivity"""

    def test_tab_header_input_str(self, config_multiple):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_multiple)
        c["tabs"][0]["tab_header_input"] = 50
        normal = normalizer.normalize(c)
        if normal["tabs"][0]["tab_header_input"] != "50":
            raise AssertionError

    def test_item_inputs_str(self, config_all_with_id):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        conf, id_ = config_all_with_id
        c = deepcopy(conf)
        if id_.find("without") == -1:
            c["tabs"][0]["items"][0]["item_inputs"].append(50)
        else:
            c["items"][0]["item_inputs"].append(50)
        normal = normalizer.normalize(c)
        for tab in normal["tabs"]:
            for item in tab["items"]:
                for entry in item["item_inputs"]:
                    if not isinstance(entry, str):
                        raise AssertionError

    def test_default_case_sensitive(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        if c.get("case_sensitive", None):
            del c["case_sensitive"]
        normal = normalizer.normalize(c)
        result = normal.get("case_sensitive", None)
        if result is None or result:
            raise AssertionError

    def test_default_screen_width(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        if c.get("screen_width", None):
            del c["screen_width"]
        normal = normalizer.normalize(c)
        result = normal.get("screen_width", None)
        if result != 80:
            raise AssertionError


@pytest.mark.integration
@pytest.mark.run(order=2)
class TestCaseInsensitive:
    """Tests that changes are made only where appropriate"""

    def test_tab_header_input_changed(self, config_multiple, random_string):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_multiple)
        c["case_sensitive"] = False
        c["tabs"][0]["tab_header_input"] = random_string
        normal = normalizer.normalize(c)
        if (
            normal["tabs"][0]["tab_header_input"] == random_string
            or normal["tabs"][0]["tab_header_input"] != random_string.lower()
        ):
            raise AssertionError

    def test_other_headers_str_but_unchanged(self, config_multiple, random_string):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_multiple)
        c["case_sensitive"] = False
        for key in ["tab_header_description", "tab_header_long_description"]:
            c["tabs"][0][key] = random_string
            normal = normalizer.normalize(c)
            if normal["tabs"][0][key] != random_string:
                raise AssertionError

    def test_other_headers_none_ok(self, config_multiple):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_multiple)
        c["case_sensitive"] = False
        for key in ["tab_header_description", "tab_header_long_description"]:
            c["tabs"][0][key] = None
            normal = normalizer.normalize(c)
            if normal["tabs"][0][key] is not None:
                raise AssertionError

    def test_other_headers_missing_ok(self, config_multiple):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_multiple)
        c["case_sensitive"] = False
        for key in ["tab_header_description", "tab_header_long_description"]:
            if key in c["tabs"][0].keys():
                del c["tabs"][0][key]
            normal = normalizer.normalize(c)
            if key in normal["tabs"][0].keys():
                raise AssertionError

    def test_choice_fields_str_but_unchanged(self, config_all_with_id, random_string):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        conf, id_ = config_all_with_id
        for key in ["item_choice_displayed", "item_description", "item_returns"]:
            c = deepcopy(conf)
            c["case_sensitive"] = False
            if id_.find("without") == -1:
                c["tabs"][0]["items"][0][key] = random_string
            else:
                c["items"][0][key] = random_string
            normal = normalizer.normalize(c)
            if normal["tabs"][0]["items"][0][key] != random_string:
                raise AssertionError

    def test_item_inputs_changed(self, config_all_with_id, random_string):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        conf, id_ = config_all_with_id
        c = deepcopy(conf)
        c["case_sensitive"] = False
        if id_.find("without") == -1:
            c["tabs"][0]["items"][0]["item_inputs"][0] = random_string
        else:
            c["items"][0]["item_inputs"][0] = random_string
        normal = normalizer.normalize(c)
        if (
            normal["tabs"][0]["items"][0]["item_inputs"][0] == random_string
            or normal["tabs"][0]["items"][0]["item_inputs"][0] != random_string.lower()
        ):
            raise AssertionError
