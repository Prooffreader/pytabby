#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylama:ignore=W293,W291,W391,E302,E128,E127,E303 (will be fixed by black)

from copy import deepcopy

import pytest

# from schema import Schema, Or, Optional

import tabbedshellmenus.validators as validators
from schema import SchemaError

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


@pytest.mark.skip  # TODO: fix this
def test_regression_ValidSchemas(data_regression):
    """Must stringify because contains schema objects"""
    data = str(validators._ValidSchemas().__dict__)
    data = {"data": data}  # apparently data_regression must use dict
    data_regression.check(data)


def test_schema_is_valid_expect_pass(input_config_dict):
    """ensures each test case passes before making them fail for different reasons"""
    validators.validate_schema(input_config_dict)


@pytest.mark.parametrize(
    "scenario",
    [
        "c['new_header'] = 'something'",
        "del c['tabs'][0]['items'][0]['choice_displayed']",
        "c['tabs'][0]['items'][0]['valid_entries'] = []",
    ],
    ids=["unexpected-top-level-header", "no-tabs.items.choice_displayed", "tabs.items.valid_entries-is-empty-list"],
)
def test_some_fail_scenarios_multiple(input_config_multiple_only, scenario):
    """Schema test should catch all of these, which are not exhaustive."""
    c = deepcopy(input_config_multiple_only)
    exec(scenario)
    with pytest.raises(SchemaError) as excinfo:
        validators.validate_schema(c)     
    #assert excinfo.value.message == 'some info'


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
    # test wrong types
    for key, value in [("case_sensitive", "string"), ("screen_width", "string")]:
        c[key] = value
    with pytest.raises(SchemaError) as excinfo:
        validators.validate_schema(c)


def test_optional_long_description_multiple(input_config_multiple_only):
    """Test that a tab's 'long_description' is optional and string"""
    c = deepcopy(input_config_multiple_only)
    validators.validate_schema(c)
    if "long_description" in c["tabs"][0].keys():
        del c["tabs"][0]["long_description"]
    else:
        c["tabs"][0]["long_description"] = "a long description"
    validators.validate_schema(c)
    # test wrong type
    c["tabs"][0]["long_description"] = 2.54
    with pytest.raises(SchemaError) as excinfo:
        validators.validate_schema(c)


@pytest.mark.parametrize("scenario", ["del c['tabs']"], ids=["no tabs"])
def test_some_fail_scenarios_single_with_key(input_config_single_with_key_only, scenario):
    """Schema test should catch all of these, which are not exhaustive."""
    c = deepcopy(input_config_single_with_key_only)
    exec(scenario)
    with pytest.raises(SchemaError) as excinfo:
        validators.validate_schema(c)


def test_no_multiple_tabs_in_single_with_key(input_config_single_with_key_only, some_random_integers):
    """Too complicated to fit in one exec statement in test_some_fail_scenarios_single_with_key"""
    str_random = str(some_random_integers)
    items = {
        "choice_displayed": "a",
        "choice_description": "a",
        "valid_entries": ["magic_text_hopefully_not_there_{}".format(str_random)],
        "returns": "magic_text_probably_not_there_".format(str_random),
    }
    c = deepcopy(input_config_single_with_key_only)
    validators.validate_schema(c)
    c["tabs"].append(items)
    with pytest.raises(SchemaError) as excinfo:
        validators.validate_schema(c)


@pytest.mark.parametrize("scenario", ["c['items'][0]['valid_entries'].append(1.5)"], ids=["float-in-valid-entries"])
def test_some_fail_scenarios_single_without_key(input_config_single_without_key_only, scenario):
    """Schema test should catch all of these, which are not exhaustive."""
    c = deepcopy(input_config_single_without_key_only)
    exec(scenario)
    with pytest.raises(SchemaError) as excinfo:
        validators.validate_schema(c)


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
    c["tabs"][0]["items"].append(c["tabs"][0]["items"][-1])
    with pytest.raises(validators.ValueOverlapError) as exc_info:
        validators.validate_no_return_value_overlap(c)


def test_validate_no_return_value_overlap_fail_within(input_config_multiple_only):
    """Add a duplicate input value within a tab"""
    c = deepcopy(input_config_multiple_only)
    c["tabs"][0]["items"].append(c["tabs"][0]["items"][-1])
    with pytest.raises(validators.ValueOverlapError) as exc_info:
        validators.validate_no_input_value_overlap(c)


def test_validate_no_return_value_overlap_fail_wtab(input_config_multiple_only):
    """Add another tab input value to a tab input"""
    c = deepcopy(input_config_multiple_only)
    extra_value = c["tabs"][0]["header_choice_displayed_and_accepted"]
    c["tabs"][1]["items"][0]["valid_entries"].append(extra_value)
    with pytest.raises(validators.ValueOverlapError) as exc_info:
        validators.validate_no_input_value_overlap(c)
