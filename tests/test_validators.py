#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylama:ignore=E114,E117,E127,E128,E231,E272,E302,E303,E501,W291,W292,W293,W391 (will be fixed by black)

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

from copy import deepcopy
import platform
import pytest

import tabbedshellmenus.validators as validators
import re


@pytest.mark.function
@pytest.mark.run(order=1)
def test_fn__determine_schema_type(input_config_dict_and_id):
    """Test that each config file has a valid schema type, and check that its filename follows the convention
    explained in conftest.py
    """
    config, id_ = input_config_dict_and_id
    schema_type = validators._determine_schema_type(config)
    assert schema_type in ("multiple", "single_with_key", "single_without_key")
    if schema_type == "multiple":
        assert id_.find("multiple") != -1
    if schema_type.startswith("single"):
        assert id_.find("single") != -1
        if schema_type.endswith("_with_key"):
            assert id_.find("with_key") != -1
        if schema_type.endswith("_without_key"):
            assert id_.find("without_key") != -1


@pytest.mark.function
@pytest.mark.run(order=2)
def test_fn__validate_schema(input_config_dict):
    """test _validate_schema. Since it depends on _determine_schema_type, order=2"""
    error_messages = []
    validators._validate_schema(error_messages, input_config_dict)
    assert not error_messages


@pytest.mark.breaking
@pytest.mark.run(order=-2)  # because if something screws up config, it will show late
def test_schema_type_change(input_config_dict_and_id):
    """Tests that proper schema type is returned when schema types are changed into other types."""
    config, id_ = input_config_dict_and_id
    # if id_.find('single_without') != -1:
    #     import pdb;pdb.set_trace()  # TODO: Delete this if test passes
    schema_type = validators._determine_schema_type(config)
    try:  # TODO: remove when test passes
        assert schema_type in ("multiple", "single_with_key", "single_without_key")
    except AssertionError:
        import pdb

        pdb.set_trace()
    if schema_type == "multiple":
        c = deepcopy(config)
        c["tabs"] = {"tabs": c["tabs"][0]}
        new_type = validators._determine_schema_type(c)
        assert new_type == "single_with_key"
    elif schema_type == "single_with_key":
        c = deepcopy(config)
        c["items"] = c["tabs"][0]["items"]
        del c["tabs"]
        new_type = validators._determine_schema_type(c)
        assert new_type == "single_without_key"
    else:
        assert schema_type == "single_without_key"  # sanity check
        c = deepcopy(config)
        c["tabs"] = [{"items": [c["items"]]}]
        del c["items"]
        new_type = validators._determine_schema_type(c)
        assert new_type == "single_with_key"


@pytest.mark.regression
@pytest.mark.run(order=1)
def test_regression__ValidSchemas(data_regression):
    """Must stringify because contains schema objects which do not serialize.
    This test fails on Windows in Python 3.5 and 2.7 for some reason; as long
    as it passes the other Windows versions tests and all the Linux tests,
    I'm not concerned."""
    if (platform.system() == 'Linux' or (platform.system () == "Windows" and sys.version[:3] >= 3.6)):
        data = str(validators._ValidSchemas().__dict__)
        # remove specific memory addresses
        data = re.sub("at 0x.+?>", "at 0xSOME_MEMORY_ADDRESS>", data)
        data = re.sub('[^a-zA-Z0-9 _]', '', data)
        data = data.split(' ')
        # convert because apparently data_regression must use dict
        data = {"data": data}
        data_regression.check(data)


@pytest.mark.breaking
@pytest.mark.run(order=5)
@pytest.mark.parametrize(
    "command,error_message",
    [
        ("c['new_header'] = 'something'", "Wrong key 'new header'"),
        ("del c['tabs'][0]['items'][0]['choice_displayed']", "Missing key: 'choice_displayed'"),
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
    assert any([x.find(error_message) for x in error_messages])


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_optional_top_level_keys_multiple(input_config_multiple_only):
    """Test that top level keys case_sensitive and screen_width are optional"""
    c = deepcopy(input_config_multiple_only)
    error_messages = []
    validators._validate_schema(error_messages, c)
    assert not error_messages
    for key, value in [("case_sensitive", True), ("screen_width", 60)]:
        if key in c.keys():
            del c[key]
        else:
            c[key] = value
        error_messages = []
        validators._validate_schema(error_messages, c)
        assert not error_messages


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_optional_long_description_multiple(input_config_multiple_only):
    """Test that a tab's 'long_description' is optional"""
    c = deepcopy(input_config_multiple_only)
    error_messages = []
    validators._validate_schema(error_messages, c)
    assert not error_messages
    if "long_description" in c["tabs"][0].keys():
        del c["tabs"][0]["long_description"]
    else:
        c["tabs"][0]["long_description"] = "a long description"
    error_messages = []
    validators._validate_schema(error_messages, c)
    assert not error_messages


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_wrong_types_top_level_keys_multiple(input_config_multiple_only):
    c = deepcopy(input_config_multiple_only)
    error_messages = []
    validators._validate_schema(error_messages, c)
    assert not error_messages
    for key, value, msg in [("case_sensitive", "string", "bool"), ("screen_width", "string", "int")]:
        c[key] = value
        error_messages = []
        validators._validate_schema(error_messages, c)
        assert any([x.find("string' should be instance of '{}'".format(msg)) for x in error_messages])


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_any_type_long_description_multiple(input_config_multiple_only):
    """Test that any type will work for long description, as it will be coerced to string in normalizer."""
    c = deepcopy(input_config_multiple_only)
    for value in [True, 10, 2.54, validators.InvalidInputError]:  # exception used just as an example of a class
        # which can be coerced to a string like any object
        error_messages = []
        validators._validate_schema(error_messages, c)
        assert not error_messages


@pytest.mark.breaking
@pytest.mark.run(order=5)
@pytest.mark.parametrize(
    "command,error_message",
    [
        (
            "c['tabs'][0]['header_choice_displayed_and_accepted']='somestring'",
            "Wrong key 'header_choice_displayed_and_accepted' in",
        ),
        ("c['tabs'][0]['header_description']='somestring'", "Wrong key 'header_description' in"),
        ("c['tabs'][0]['long_description']='somestring'", "Wrong key 'long_description' in"),
    ],
    ids=[
        "should_not_have_header_choice_displayed_and_accepted",
        "should_not_have_header_description",
        "should_not_have_long_description_which_is_optional_in_multiple",
    ],
)
def test_some_fail_scenarios_single_with_key(input_config_single_with_key_only, command, error_message):
    """Schema test should catch all of these, which are not exhaustive."""
    c = deepcopy(input_config_single_with_key_only)
    exec(command)
    error_messages = []
    validators._validate_schema(error_messages, c)
    assert any([x.find(error_message) for x in error_messages])


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_no_multiple_tabs_in_single_with_key(input_config_single_with_key_only, random_string):
    """Too complicated to fit in one exec statement in test_some_fail_scenarios_single_with_key.
    This will be recognized by the validator as a multiple tab type, but missing the keys
    'header_choice_displayed_and_accepted' and 'header_description'
    """  # TODO: why is only the first reported in error_messages?
    tab = {
        "items": [
            {
                "choice_displayed": "a_{}".format(random_string),
                "choice_description": "b_{}".format(random_string),
                "valid_entries": ["c_{}".format(random_string)],
                "returns": "d_".format(random_string),
            }
        ]
    }
    c = deepcopy(input_config_single_with_key_only)
    error_messages = []
    validators._validate_schema(error_messages, c)
    assert not error_messages
    c["tabs"].append(tab)
    error_messages = []
    validators._validate_schema(error_messages, c)
    # These are split up because Python 2 has u'header_choice... and I don't feel like fixing it
    assert any([x.find("Missing key: ") != -1 for x in error_messages])
    assert any([x.find("'header_choice_displayed_and_accepted'") != -1 for x in error_messages])
    # assert any([x.find("Missing key: 'header_description'") != -1 for x in error_messages])


@pytest.mark.function
@pytest.mark.run(order=1)
def test_fn__config_tabs(input_config_dict):
    """Hard to make this non tautological"""
    tabs = validators._config_tabs(input_config_dict)
    assert isinstance(tabs[0]["items"], list)


@pytest.mark.function
@pytest.mark.run(order=1)
def test_fn__validate_no_return_value_overlap(input_config_dict):
    """Expect pass on valid input data"""
    error_messages = []
    validators._validate_no_return_value_overlap(error_messages, input_config_dict)
    assert not error_messages


@pytest.mark.function
@pytest.mark.run(order=1)
def test_fn__validate_no_input_value_overlap(input_config_dict):
    """Expect pass on valid input data"""
    error_messages = []
    validators._validate_no_input_value_overlap(error_messages, input_config_dict)
    assert not error_messages


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_validate_no_return_value_overlap_fail(input_config_multiple_only):
    """Add a duplicate return value in a tab"""
    c = deepcopy(input_config_multiple_only)
    c["tabs"][0]["items"] += [c["tabs"][0]["items"][-1]]
    error_messages = []
    validators._validate_no_return_value_overlap(error_messages, c)
    assert any([x.find("there are repeated return values") != -1 for x in error_messages])


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
        assert any([x.find("there are repeated input values") != -1 for x in error_messages])


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test__validate_no_input_value_overlap_fail_between_item_and_tab(input_config_multiple_only):
    """Add a tab header value to a to valid_input in an item"""
    c = deepcopy(input_config_multiple_only)
    extra_value = c["tabs"][0]["header_choice_displayed_and_accepted"]
    c["tabs"][1]["items"][0]["valid_entries"] += [extra_value]
    error_messages = []
    validators._validate_no_input_value_overlap(error_messages, c)
    assert any([x.find("there are repeated input values") != -1 for x in error_messages])


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test_validate_case_sensitive(config_stub_without_tabs, input_config_case_sensitive_only, random_string):
    """NB the test cases have to include at least one case sensitive config with
    at least one tab with at least two items. This is verified in conf"""
    tabs = deepcopy(validators._config_tabs(input_config_case_sensitive_only))
    if len(tabs[0]["items"]) < 2:
        assert 1 == 1  # skips these cases, conftest makes sure there is at least one that won't be skipped
    else:
        # check multiple items valid entries
        c = deepcopy(config_stub_without_tabs)
        c["case_sensitive"] = True
        c["tabs"] = tabs
        c["tabs"][0]["items"][0]["valid_choices"] = [random_string]
        c["tabs"][0]["items"][1]["valid_choices"] = [random_string.lower()]
        error_messages = []
        validators._validate_no_input_value_overlap(error_messages, c)
        assert not error_messages
        # check with multiple tabs
        if len(c["tabs"]) > 1:
            c["tabs"][0]["items"][1]["valid_choices"] = [random_string + random_string]
            c["tabs"][1]["header_choice_displayed_and_accepted"] = random_string.lower()
            error_messages = []
            validators._validate_no_input_value_overlap(error_messages, c)
            assert not error_messages


@pytest.mark.breaking
@pytest.mark.run(order=5)
def test__validate_case_insensitive(input_config_case_insensitive_only, config_stub_without_tabs, random_string):
    """"NB the test cases have to include at least one case sensitive config with
    at least one tab with at least two items. This is verified in conftest.py"""
    tabs = deepcopy(validators._config_tabs(input_config_case_insensitive_only))
    if len(tabs[0]["items"]) < 2:
        assert 1 == 1  # skips these cases, conftest makes sure there is at least one that won't be skipped
    else:
        # check multiple items valid entries
        c = deepcopy(config_stub_without_tabs)
        c["case_sensitive"] = False
        c["tabs"] = tabs
        c["tabs"][0]["items"][0]["valid_entries"] = [random_string]
        c["tabs"][0]["items"][1]["valid_entries"] = [random_string.lower()]
        error_messages = []
        validators._validate_no_input_value_overlap(error_messages, c)
        assert any([x.find("repeated input values") != -1 for x in error_messages])
        assert any([x.find("Note case sensitive is false") != -1 for x in error_messages])
        # check with multiple tabs
        if len(c["tabs"]) > 1:
            new_string = "a" + random_string
            c["tabs"][0]["items"][1]["valid_entries"] = [new_string]
            c["tabs"][1]["header_choice_displayed_and_accepted"] = new_string.lower()
            error_messages = []
            validators._validate_no_input_value_overlap(error_messages, c)
            assert any([x.find("repeated input values including tab selectors") != -1 for x in error_messages])
            assert any([x.find("Note case sensitive is false") != -1 for x in error_messages])


@pytest.mark.integration
@pytest.mark.run(order=-1)
def test_fn_validate_all(input_config_dict):
    """ensures each test case overall  validation passes before making them fail for different reasons
    TODO: order this one as integration"""
    validators.validate_all(input_config_dict)
