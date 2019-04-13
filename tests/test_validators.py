#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests tabbedshellmenus/validators.py"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pprint
import re
import sys
from copy import deepcopy

import pytest

import tabbedshellmenus.validators as validators


@pytest.mark.function
@pytest.mark.run(order=1)
def test_fn__determine_schema_type(input_config_dict_and_id):
    """Test that each config file has a valid schema type, and check that its filename follows convention

    The convention is explained in conftest.py
    """
    config, id_ = input_config_dict_and_id
    schema_type = validators._determine_schema_type(config)
    if schema_type not in ("multiple", "single_with_key", "single_without_key"):
        raise AssertionError("Unrecognized schema_type")
    if schema_type == "multiple":
        if id_.find("multiple") == -1:
            raise AssertionError("this schema type should include multiple")
    if schema_type.startswith("single"):
        if id_.find("single") == -1:
            raise AssertionError("this schema type should include single")
        if schema_type.endswith("_with_key"):
            if id_.find("with_key") == -1:
                raise AssertionError("this schema type should include with_key")
        if schema_type.endswith("_without_key"):
            if id_.find("without_key") == -1:
                raise AssertionError("this schema type should include with_key")


@pytest.mark.function
@pytest.mark.run(order=2)
def test_fn__validate_schema(input_config_dict):
    """Test _validate_schema. Since it depends on _determine_schema_type, order=2"""
    error_messages = []
    validators._validate_schema(error_messages, input_config_dict)
    if error_messages:
        raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=-2)  # because if something screws up config, it will show late
def test_schema_type_change(input_config_dict):
    """Tests that proper schema type is returned when schema types are changed into other types."""
    config = input_config_dict
    schema_type = validators._determine_schema_type(config)
    if schema_type not in ("multiple", "single_with_key", "single_without_key"):
        raise AssertionError
    if schema_type == "multiple":
        c = deepcopy(config)
        c["tabs"] = {"tabs": c["tabs"][0]}
        new_type = validators._determine_schema_type(c)
        if not new_type == "single_with_key":
            raise AssertionError
    elif schema_type == "single_with_key":
        c = deepcopy(config)
        c["items"] = c["tabs"][0]["items"]
        del c["tabs"]
        new_type = validators._determine_schema_type(c)
        if not new_type == "single_without_key":
            raise AssertionError
    else:
        if not schema_type == "single_without_key":  # sanity check
            raise AssertionError("schema_type wrong")
        c = deepcopy(config)
        c["tabs"] = [{"items": [c["items"]]}]
        del c["items"]
        new_type = validators._determine_schema_type(c)
        if not new_type == "single_with_key":
            raise AssertionError


@pytest.mark.regression
@pytest.mark.run(order=1)
def test_regression__ValidSchemas_py36plus(data_regression):
    """Must stringify because contains schema objects which do not serialize."""
    if sys.version[:3] >= "3.6":
        data = pprint.pformat(validators._ValidSchemas().__dict__)
        # remove specific memory addresses
        data = re.sub("at 0x.+?>", "at 0xSOME_MEMORY_ADDRESS>", data)
        data = re.sub("[^a-zA-Z0-9 _]", "", data)
        data = data.split(" ")
        # convert because apparently data_regression must use dict
        data = {"data": data}
        data_regression.check(data)


@pytest.mark.regression
@pytest.mark.run(order=1)
def test_regression__ValidSchemas_py27(data_regression):
    """Sorted because as long as it passes in Python 3.6+ this is just extra"""
    if sys.version[:3] == "2.7":
        data = pprint.pformat(validators._ValidSchemas().__dict__).lower().replace("_", "\n")
        # remove specific memory addresses
        data = re.sub("at 0x.+?>", "", data)
        data = re.sub("[^a-zA-Z0-9]", "\n", data)
        data = re.sub("u", "", data)
        data = sorted(set(data.split("\n")))
        # convert because apparently data_regression must use dict
        data = {"data": data}
        data_regression.check(data)


@pytest.mark.regression
@pytest.mark.run(order=1)
def test_regression__ValidSchemas_py35(data_regression):
    """Sorted because as long as it passes in Python 3.6+ this is just extra"""
    if sys.version[:3] == "3.5":
        data = pprint.pformat(validators._ValidSchemas().__dict__).lower().replace("_", "\n")
        # remove specific memory addresses
        data = re.sub("at 0x.+?>", "", data)
        data = re.sub("[^a-zA-Z0-9]", "\n", data)
        data = sorted(set(data.split("\n")))
        # convert because apparently data_regression must use dict
        data = {"data": data}
        data_regression.check(data)


@pytest.mark.breaking
@pytest.mark.run(order=5)
@pytest.mark.parametrize(
    "command,error_message",
    [
        ("c['new_header'] = 'something'", "Wrong key .{0,1}'new_header'"),
        ("del c['tabs'][0]['items'][0]['choice_displayed']", "Missing key: .{0,1}'choice_displayed'"),
        ("c['tabs'][0]['items'][0]['valid_entries'] = []", "should evaluate to True"),
    ],
    ids=["unexpected_top_level_header", "no_tabs.items.choice_displayed", "tabs.items.valid_entries_is_empty_list"],
)
def test_some_fail_scenarios_multiple(input_config_multiple_only, command, error_message):
    """Schema test should catch all of these, which are not exhaustive."""
    c = deepcopy(input_config_multiple_only)
    exec(command)
    error_messages = []
    validators._validate_schema(error_messages, c)
    if not any([re.search(error_message, x) for x in error_messages]):
        raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_optional_top_level_keys_multiple(input_config_multiple_only):
    """Test that top level keys case_sensitive and screen_width are optional"""
    c = deepcopy(input_config_multiple_only)
    error_messages = []
    validators._validate_schema(error_messages, c)
    if error_messages:
        raise AssertionError
    for key, value in [("case_sensitive", True), ("screen_width", 60)]:
        if key in c.keys():
            del c[key]
        else:
            c[key] = value
        error_messages = []
        validators._validate_schema(error_messages, c)
        if error_messages:
            raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_optional_header_long_description_multiple(input_config_multiple_only):
    """Test that a tab's 'header_long_description' is optional"""
    c = deepcopy(input_config_multiple_only)
    error_messages = []
    validators._validate_schema(error_messages, c)
    if error_messages:
        raise AssertionError
    if "header_long_description" in c["tabs"][0].keys():
        del c["tabs"][0]["header_long_description"]
    else:
        c["tabs"][0]["header_long_description"] = "a long description"
    error_messages = []
    validators._validate_schema(error_messages, c)
    if error_messages:
        raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_wrong_types_top_level_keys_multiple(input_config_multiple_only):
    """Ensure wrong types are caught."""
    c = deepcopy(input_config_multiple_only)
    error_messages = []
    validators._validate_schema(error_messages, c)
    if error_messages:
        raise AssertionError
    for key, value, msg in [("case_sensitive", "string", "bool"), ("screen_width", "string", "int")]:
        c = deepcopy(input_config_multiple_only)
        c[key] = value
        error_messages = []
        validators._validate_schema(error_messages, c)
        if all([x.find("string' should be instance of '{}'".format(msg)) == -1 for x in error_messages]):
            raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_any_type_header_long_description_multiple(input_config_multiple_only):
    """Test that any type will work for long description, as it will be coerced to string in normalizer."""
    c = deepcopy(input_config_multiple_only)
    for value in [True, 10, 2.54, KeyError, None]:  # exception used just as an example of a class
        # which can be coerced to a string like any object
        c["tabs"][0]["header_long_description"] = value
        error_messages = []
        validators._validate_schema(error_messages, c)
        if error_messages:
            raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=5)
@pytest.mark.parametrize(
    "command,error_message",
    [
        (
            "c['tabs'][0]['header_entry']='somestring'",
            "Forbidden key encountered: .{0,1}'header_entry'",
        ),
        ("c['tabs'][0]['header_description']='somestring'", "Forbidden key encountered: .{0,1}'header_description'"),
        ("c['tabs'][0]['header_long_description']='somestring'", "Forbidden key encountered: .{0,1}'header_long_description'"),
    ],
    ids=[
        "should_not_have_header_entry",
        "should_not_have_header_description",
        "should_not_have_header_long_description_which_is_optional_in_multiple",
    ],
)
def test_some_fail_scenarios_single_with_key(input_config_single_with_key_only, command, error_message):
    """Schema test should catch all of these, which are not exhaustive."""
    c = deepcopy(input_config_single_with_key_only)
    exec(command)
    error_messages = []
    validators._validate_schema(error_messages, c)
    if not any([re.search(error_message, x) for x in error_messages]):
        raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_no_multiple_tabs_in_single_with_key(input_config_single_with_key_only, random_string):
    """Too complicated to fit in one exec statement in test_some_fail_scenarios_single_with_key.

    This will be recognized by the validator as a multiple tab type, but missing the keys
    'header_entry' and 'header_description'
    """
    tab = {
        "items": [
            {
                "choice_displayed": "a_{}".format(random_string),
                "choice_description": "b_{}".format(random_string),
                "valid_entries": ["c_{}".format(random_string)],
                "returns": "d_{}".format(random_string),
            }
        ]
    }
    c = deepcopy(input_config_single_with_key_only)
    error_messages = []
    validators._validate_schema(error_messages, c)
    if error_messages:
        raise AssertionError
    c["tabs"].append(tab)
    error_messages = []
    validators._validate_schema(error_messages, c)
    # These are split up because Python 2 has u'header_choice... and I don't feel like fixing it
    if not (
        any([x.find("Missing key: ") != -1 for x in error_messages])
        or any([x.find("'header_entry'") != -1 for x in error_messages])
    ):
        raise AssertionError


@pytest.mark.function
@pytest.mark.run(order=1)
def test_fn__config_tabs(input_config_dict):
    """Hard to make this non tautological"""
    tabs = validators._config_tabs(input_config_dict)
    if not isinstance(tabs[0]["items"], list):
        raise AssertionError()


@pytest.mark.function
@pytest.mark.run(order=1)
def test_fn__validate_no_return_value_overlap(input_config_dict):
    """Expect pass on valid input data"""
    error_messages = []
    validators._validate_no_return_value_overlap(error_messages, input_config_dict)
    if not all([x.find("there are repeated return values") == -1 for x in error_messages]):
        raise AssertionError


@pytest.mark.function
@pytest.mark.run(order=1)
def test_fn__validate_no_input_value_overlap(input_config_dict):
    """Expect pass on valid input data"""
    error_messages = []
    validators._validate_no_input_value_overlap(error_messages, input_config_dict)
    if not all([x.find("repeated input values") == -1 for x in error_messages]):
        raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_validate_no_return_value_overlap_fail(input_config_multiple_only):
    """Add a duplicate return value in a tab"""
    c = deepcopy(input_config_multiple_only)
    c["tabs"][0]["items"] += [c["tabs"][0]["items"][-1]]
    error_messages = []
    validators._validate_no_return_value_overlap(error_messages, c)
    if all([x.find("there are repeated return values") == -1 for x in error_messages]):
        raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_validate_no_input_value_overlap_fail_within_an_item(
    input_config_multiple_only, input_config_single_with_key_only
):
    """Add a duplicate valid_input value within an item"""
    for input_ in (input_config_multiple_only, input_config_single_with_key_only):
        c = deepcopy(input_)
        c["tabs"][0]["items"] += [c["tabs"][0]["items"][-1]]
        error_messages = []
        validators._validate_no_input_value_overlap(error_messages, c)
        if all([x.find("there are repeated input values") == -1 for x in error_messages]):
            raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test__validate_no_input_value_overlap_fail_between_item_and_tab(input_config_multiple_only):
    """Add a tab header value to a to valid_input in an item"""
    c = deepcopy(input_config_multiple_only)
    extra_value = c["tabs"][0]["header_entry"]
    c["tabs"][1]["items"][0]["valid_entries"] += [extra_value]
    error_messages = []
    validators._validate_no_input_value_overlap(error_messages, c)
    if all([x.find("there are repeated input values") == -1 for x in error_messages]):
        raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_validate_case_sensitive(config_stub_without_tabs, input_config_case_sensitive_only, random_string):
    """Tests case_sensitive configs for case sensitivity.

    NB the test cases have to include at least one case sensitive config with
    at least one tab with at least two items. This is verified in conf
    """
    tabs = deepcopy(validators._config_tabs(input_config_case_sensitive_only))
    if len(tabs[0]["items"]) < 2:
        return  # skips these cases, conftest makes sure there is at least one that won't be skipped:
    else:
        # check multiple items valid entries
        c = deepcopy(config_stub_without_tabs)
        c["case_sensitive"] = True
        c["tabs"] = tabs
        c["tabs"][0]["items"][0]["valid_choices"] = [random_string]
        c["tabs"][0]["items"][1]["valid_choices"] = [random_string.lower()]
        error_messages = []
        validators._validate_no_input_value_overlap(error_messages, c)
        if error_messages:
            raise AssertionError
        # check with multiple tabs
        if len(c["tabs"]) > 1:
            c["tabs"][0]["items"][1]["valid_choices"] = [random_string + random_string]
            c["tabs"][1]["header_entry"] = random_string.lower()
            error_messages = []
            validators._validate_no_input_value_overlap(error_messages, c)
            if error_messages:
                raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test__validate_case_insensitive(input_config_case_insensitive_only, config_stub_without_tabs, random_string):
    """Tests case-insensitive configs for case insensitivity

    NB the test cases have to include at least one case sensitive config with
    at least one tab with at least two items. This is verified in conftest.py
    """
    tabs = deepcopy(validators._config_tabs(input_config_case_insensitive_only))
    if len(tabs[0]["items"]) < 2:
        return  # skips these cases, conftest makes sure there is at least one that won't be skipped:
    else:
        # check multiple items valid entries
        c = deepcopy(config_stub_without_tabs)
        c["case_sensitive"] = False
        c["tabs"] = tabs
        c["tabs"][0]["items"][0]["valid_entries"] = [random_string]
        c["tabs"][0]["items"][1]["valid_entries"] = [random_string.lower()]
        error_messages = []
        validators._validate_no_input_value_overlap(error_messages, c)
        if all([x.find("repeated input values") == -1 for x in error_messages]):
            raise AssertionError
        if all([x.find("Note case sensitive is false") == -1 for x in error_messages]):
            raise AssertionError
        # check with multiple tabs
        if len(c["tabs"]) > 1:
            new_string = "a" + random_string
            c["tabs"][0]["items"][1]["valid_entries"] = [new_string]
            c["tabs"][1]["header_entry"] = new_string.lower()
            error_messages = []
            validators._validate_no_input_value_overlap(error_messages, c)
            if not (
                any([x.find("repeated input values including tab selectors") != -1 for x in error_messages])
                or any([x.find("Note case sensitive is false") != -1 for x in error_messages])
            ):
                raise AssertionError()


@pytest.mark.integration
@pytest.mark.run(order=-1)
def test_fn_validate_all(input_config_dict):
    """Ensures each test case overall  validation passes before making them fail for different reasons

    TODO: order this one as integration
    """
    validators.validate_all(input_config_dict)
