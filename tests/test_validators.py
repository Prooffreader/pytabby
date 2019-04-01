#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylama:ignore=W293,W291,W391,E302,E128,E127,E303,E501 (will be fixed by black)

from copy import deepcopy

import pytest

import tabbedshellmenus.validators as validators
import schema
import re

pytest_plugins = ("regressions",)


def test__determine_schema_type(input_config_dict_and_id):
    """As long as naming convention of test files stated in <root>/tests/data are followed, this should
    pass, and that was tested in conftest.py
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


def test_regression_ValidSchemas(data_regression):
    """Must stringify because contains schema objects"""
    data = str(validators._ValidSchemas().__dict__)
    # remove specific memory addresses
    data = re.sub(' at 0x[a-f0-9]+>', 'at 0xSOME_MEMORY_ADDRESS>', data)
     # convert because apparently data_regression must use dict
    data = {"data": data} 
    data_regression.check(data)


def test_schema_is_valid_expect_pass(input_config_dict):
    """ensures each test case passes before making them fail for different reasons"""
    validators.validate_schema(input_config_dict)


@pytest.mark.parametrize(
    "command,error_class,error_message",
    [
        ("c['new_header'] = 'something'", schema.SchemaWrongKeyError, "Wrong key 'new header'"),
        ("del c['tabs'][0]['items'][0]['choice_displayed']", schema.SchemaMissingKeyError, "Missing key: 'choice_displayed'"),
        ("c['tabs'][0]['items'][0]['valid_entries'] = []", schema.SchemaError, "should evaluate to True")
    ],
    ids=["unexpected_top_level_header", "no_tabs.items.choice_displayed", "tabs.items.valid_entries_is_empty_list"],
)
def test_some_fail_scenarios_multiple(input_config_multiple_only, command, error_class, error_message):
    """Schema test should catch all of these, which are not exhaustive."""
    c = deepcopy(input_config_multiple_only)
    exec(command)
    with pytest.raises(error_class) as exc_info:
        validators.validate_schema(c)     
        assert exc_info.value.message.find(error_message)


def test_optional_top_level_keys_multiple(input_config_multiple_only):
    """Test that top level keys case_sensitive and screen_width are optional
    and the correct types"""
    c = deepcopy(input_config_multiple_only)
    validators.validate_schema(c)
    for key, value in [("case_sensitive", True), ("screen_width", 60)]:
        if key in c.keys():
            del c[key]
        else:
            c[key] = value
        validators.validate_schema(c)

def test_wrong_types_top_level_keys_multiple(input_config_multiple_only):
    c = deepcopy(input_config_multiple_only)
    validators.validate_schema(c)
    for key, value, msg in [("case_sensitive", "string", "bool"), ("screen_width", "string", "int")]:
        c[key] = value
    with pytest.raises(schema.SchemaError) as exc_info:
        validators.validate_schema(c)
        assert exc_info.value.message.find("string' should be instance of '{}'".format(msg))


def test_optional_long_description_multiple(input_config_multiple_only):
    """Test that a tab's 'long_description' is optional and string"""
    c = deepcopy(input_config_multiple_only)
    validators.validate_schema(c)
    if "long_description" in c["tabs"][0].keys():
        del c["tabs"][0]["long_description"]
    else:
        c["tabs"][0]["long_description"] = "a long description"
    validators.validate_schema(c)

def test_wrong_type_long_description_multiple(input_config_multiple_only):
    c = deepcopy(input_config_multiple_only)
    validators.validate_schema(c)
    c["tabs"][0]["long_description"] = 2.54
    with pytest.raises(schema.SchemaError) as exc_info:
        validators.validate_schema(c)
        assert exc_info.value.message.find("should be instance of 'str'")


@pytest.mark.parametrize(
    "command,error_class,error_message",
    [
        ("c['items']=c['tabs'][0]['items'];del c['tabs']", TypeError, "'NoneType' object is not subscriptable"),
        ("c['tabs'][0]['header_choice_displayed_and_accepted']='somestring'", schema.SchemaWrongKeyError, 
        "Wrong key 'header_choice_displayed_and_accepted' in"),
        ("c['tabs'][0]['header_description']='somestring'", schema.SchemaWrongKeyError, 
        "Wrong key 'header_description' in"),
        ("c['tabs'][0]['long_description']='somestring'", schema.SchemaWrongKeyError, 
        "Wrong key 'long_description' in")
    ],
    ids=["made_into_without_key",
         "has_header_choice_displayed_and_accepted",
         "has_header_description",
         "has_long_description_which_is_optional_in_multiple"],
)
def test_some_fail_scenarios_single_with_key(input_config_single_with_key_only, command, error_class, error_message):
    """Schema test should catch all of these, which are not exhaustive."""
    c = deepcopy(input_config_single_with_key_only)
    exec(command)
    if error_message == 'interrupt':  # for test development
        validators.validate_schema(c)
    with pytest.raises(error_class) as exc_info:
        validators.validate_schema(c)     
        assert exc_info.value.message.find(error_message)

def test_no_multiple_tabs_in_single_with_key(input_config_single_with_key_only, random_string):
    """Too complicated to fit in one exec statement in test_some_fail_scenarios_single_with_key.
    This will be recognized by the validator as a multiple tab type, but missing the keys
    'header_choice_displayed_and_accepted' and 'header_description'"""
    tab = {'items': {
        "choice_displayed": "a_{}".format(random_string),
        "choice_description": "a_{}".format(random_string),
        "valid_entries": ["magic_text_hopefully_not_there_{}".format(random_string)],
        "returns": "magic_text_probably_not_there_".format(random_string),
    }}
    c = deepcopy(input_config_single_with_key_only)
    validators.validate_schema(c)
    c["tabs"].append(tab)
    with pytest.raises(schema.SchemaMissingKeyError) as exc_info:
        validators.validate_schema(c)
        assert exc_info.value.message.find("Missing keys: 'header_choice_displayed_and_accepted', 'header_description'")

@pytest.mark.parametrize(
    "command,error_class,error_message",
    [
        ("c['items'][0]['valid_entries']+=[1.5]", schema.SchemaError, "did not validate 1.5")
    ],
    ids=["float_in_valid_entries"],
)
def test_some_fail_scenarios_single_without_key(input_config_single_without_key_only, command, error_class, 
        error_message):
    """Schema test should catch all of these, which are not exhaustive."""
    c = deepcopy(input_config_single_without_key_only)
    exec(command)
    if error_message == 'interrupt':  # for test development
        validators.validate_schema(c)
    with pytest.raises(error_class) as exc_info:
        validators.validate_schema(c)     
        assert exc_info.value.message.find(error_message)


def test__config_tabs(input_config_dict):
    """Hard to make this non tautological"""
    tabs = validators._config_tabs(input_config_dict)
    assert isinstance(tabs[0]["items"], list)


def test_validate_no_return_value_overlap(input_config_dict):
    """Expect pass on valid input data"""
    validators.validate_no_return_value_overlap(input_config_dict)


def test_validate_no_input_value_overlap(input_config_dict):
    """Expect pass on valid input data"""
    validators.validate_no_input_value_overlap(input_config_dict)


def test_validate_no_return_value_overlap_fail(input_config_multiple_only):
    """Add a duplicate return value in a tab"""
    c = deepcopy(input_config_multiple_only)
    c["tabs"][0]["items"] += [c["tabs"][0]["items"][-1]]
    with pytest.raises(validators.ValueOverlapError):
        # no exc_info because I'm in charge of that message
        validators.validate_no_return_value_overlap(c)


def test_validate_no_return_value_overlap_fail_within(input_config_multiple_only):
    """Add a duplicate input value within a tab"""
    c = deepcopy(input_config_multiple_only)
    c["tabs"][0]["items"] += [c["tabs"][0]["items"][-1]]
    with pytest.raises(validators.ValueOverlapError):
        # no exc_info because I'm in charge of that message
        validators.validate_no_input_value_overlap(c)


def test_validate_no_return_value_overlap_fail_wtab(input_config_multiple_only):
    """Add another tab input value to a tab input"""
    c = deepcopy(input_config_multiple_only)
    extra_value = c["tabs"][0]["header_choice_displayed_and_accepted"]
    c["tabs"][1]["items"][0]["valid_entries"] += [extra_value]
    with pytest.raises(validators.ValueOverlapError):
        # no exc_info because I'm in charge of that message
        validators.validate_no_input_value_overlap(c)


def test_validate_case_sensitive(input_config_case_sensitive_only, random_string):
    """NB in conftest.py, skips those without a tab key
    NB the test cases have to include at least one case sensitive config with
    at least one tab with at least two items"""
    if len(input_config_case_sensitive_only['tabs'][0]['items']) < 2:
        assert 1 == 1
    else:
        # check multiple items valid entries
        c = deepcopy(input_config_case_sensitive_only)
        c['tabs'][0]['items'][0]['valid_choices'] = [random_string]
        c['tabs'][0]['items'][1]['valid_choices'] = [random_string.lower()]
        validators.validate_no_input_value_overlap(c)
        # check with multiple tabs
        if len(c['tabs']) > 1:
            c['tabs'][0]['items'][1]['valid_choices'] = [random_string+random_string]
            c['tabs'][1]['header_choice_displayed_and_accepted'] = random_string.lower()
            validators.validate_no_input_value_overlap(c)

# DOES NOT WORK; NEED BRANCH TO FIX CASE-SENSITIVE AND OTHERWISE NORMALIZE

# def test_validate_case_insensitive(input_config_case_insensitive_only, random_string):
#     """NB in conftest.py, skips those without a tab key
#     NB the test cases have to include at least one case sensitive config with
#     at least one tab with at least two items"""
#     if len(input_config_case_insensitive_only['tabs'][0]['items']) < 2:
#         assert 1 == 1
#     else:
#         # check multiple items valid entries
#         c = deepcopy(input_config_case_insensitive_only)
#         import pdb;pdb.set_trace()
#         c['tabs'][0]['items'][0]['valid_choices'] = [random_string]
#         c['tabs'][0]['items'][1]['valid_choices'] = [random_string.lower()]
#         validators.validate_no_input_value_overlap(c)
#         # check with multiple tabs
#         if len(c['tabs']) > 1:
#             c['tabs'][0]['items'][1]['valid_choices'] = [random_string+random_string]
#             c['tabs'][1]['header_choice_displayed_and_accepted'] = random_string.lower()
#             validators.validate_no_input_value_overlap(c)


