#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests tabbedshellmenus/validators.py"""



from copy import deepcopy

import pytest

import tabbedshellmenus.validators as validators

# HELPER FUNCTIONS #


def del_key_if_present(dict_, key):
    """Returns dict with deleted key if it was there, otherwise unchanged dict"""
    if key in dict_.keys():
        del dict_[key]
    return dict_


# helper functions for breaking tests


def validate_schema_fail(conf, expected_error_message_parts, case=None):
    """Boilerplate to validate the failure of a schema"""
    error_messages = []
    error_messages = validators._validate_schema(error_messages, conf)
    if len(error_messages) != 1:
        raise AssertionError("There should be one error message, not {0}".format(len(error_messages)))
    for message in expected_error_message_parts:
        if error_messages[0].find(message) == -1:
            if case:
                msg = "CASE {0} MISSING IN ERROR MESSAGES: {1}".format(case, message)
            else:
                msg = "MISSING IN ERROR MESSAGES: {0}".format(message)
            raise AssertionError(msg)


def validate_iteration_fail(conf, expected_error_message_part, case=None):
    """Boilerplate to validate the failure of iteration during a schema check

    Note there may be multiple errors, this will only check if the iteration error appears.
    """
    error_messages = []
    error_messages = validators._validate_schema(error_messages, conf)
    if validators._determine_config_layout(conf) is None:
        error_messages.append("Schema type not recognized")
    found = False
    for error_message in error_messages:
        if error_message.find(expected_error_message_part) != -1:
            found = True
    if not found:
        if case:
            msg = "CASE {0} MISSING IN ERROR MESSAGES: {1}".format(case, "; ".join(error_messages))
        else:
            msg = "MISSING IN ERROR MESSAGES: {0}".format("; ".join(error_messages))
        raise AssertionError(msg)


# TESTS OF SINGLE FUNCTIONS


@pytest.mark.function
@pytest.mark.run(order=1)
def test_fn__determine_config_layout(config_all_with_id):
    """Test that all config dicts return a valid type, and that it matches id"""
    config, id_ = config_all_with_id
    config_layout = validators._determine_config_layout(config)
    if config_layout not in ("multiple", "single_with_key", "single_without_key"):
        raise AssertionError("Unrecognized config_layout")
    if config_layout == "multiple":
        if id_.find("multiple") == -1:
            raise AssertionError("this id should include multiple")
    if config_layout.startswith("single"):
        if id_.find("single") == -1:
            raise AssertionError("this id should include single")
        if config_layout.endswith("_with_key"):
            if id_.find("with_key") == -1:
                raise AssertionError("this id should include with_key")
        if config_layout.endswith("_without_key"):
            if id_.find("without_key") == -1:
                raise AssertionError("this id should include with_key")


@pytest.mark.integration
@pytest.mark.run(order=2)  # order 2 because it depends on determine_config_layout(), and breaking tests depend on it
def test_fn__validate_schema(config_all):
    """Test _validate_schema. Since it depends on _determine_config_layout, order=2"""
    error_messages = []
    error_messages = validators._validate_schema(error_messages, config_all)
    if error_messages:
        raise AssertionError("config did not pass initial schema check")


# TESTS CLASSES: TOP-LEVEL KEYS
# NONBREAKING, THEN BREAKING
@pytest.mark.function
@pytest.mark.run(order=2)
class TestSchemaTop:
    """Goes through all allowed values in the top level of configs"""

    def test_case_sensitive_missing(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        c = del_key_if_present(c, "case_sensitive")
        error_messages = []
        error_messages = validators._validate_schema(error_messages, c)
        if error_messages:
            raise AssertionError(error_messages)

    def test_case_sensitive_bool(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        for case in [True, False]:
            c["case_sensitive"] = case
            error_messages = []
            error_messages = validators._validate_schema(error_messages, c)
            if error_messages:
                raise AssertionError(case)

    def test_screen_width_missing(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        c = del_key_if_present(c, "screen_width")
        error_messages = []
        error_messages = validators._validate_schema(error_messages, c)
        if error_messages:
            raise AssertionError(error_messages)

    def test_screen_width_int(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        c["screen_width"] = 40
        error_messages = []
        error_messages = validators._validate_schema(error_messages, c)
        if error_messages:
            raise AssertionError(error_messages)

    def test_multiple_tabs(self, config_multiple):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        if not len(config_multiple["tabs"]) > 1:
            raise AssertionError  # probably tautological but wth; actually might fail if test_config not


@pytest.mark.breaking
@pytest.mark.run(order=3)
class TestBreakingSchemaTop:
    """Performs schema-invalidating changes on all config"""

    def test_wrong_type_case_sensitive(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        for case in ["string", -1, 2, 1.5, bool]:
            c["case_sensitive"] = case
            validate_schema_fail(
                c, ["schema.SchemaError: Key 'case_sensitive' error:", "should be instance of 'bool'"], case
            )

    def test_wrong_type_invalid_screen_width(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        for case in ["string", 80.3, int]:
            c["screen_width"] = case
            validate_schema_fail(
                c, ["schema.SchemaError: Key 'screen_width' error:", "should be instance of 'int'"], case
            )

    def test_lambda_invalid_screen_width(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        for case in [-1, 0]:
            c["screen_width"] = case
            validate_schema_fail(
                c, ["schema.SchemaError: Key 'screen_width' error:", "<lambda", "should evaluate to True"], case
            )

    def test_missing_tabs(self, config_multiple, config_single_with_key):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for config in [config_multiple, config_single_with_key]:
            c = deepcopy(config)
            del c["tabs"]
            # note that schema type identifier now thinks this is a single_without_key
            validate_iteration_fail(c, "WHILE ITERATING OVER items: KeyError:")

    def test_wrong_type_tabs_not_iterable(self, config_multiple, config_single_with_key):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for config in [config_multiple, config_single_with_key]:
            c = deepcopy(config)
            for case in [{0, 1}, {0: 1}, []]:
                c["tabs"] = case
                validate_iteration_fail(c, "No further introspection possible", repr(case))

    def test_wrong_type_tabs_string(self, config_multiple, config_single_with_key):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for config in [config_multiple, config_single_with_key]:
            c = deepcopy(config)
            for case in ["string", ""]:
                c["tabs"] = case
                validate_iteration_fail(c, "No further introspection possible.", case)

    def test_wrong_type_tabs_other(self, config_multiple, config_single_with_key):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for config in [config_multiple, config_single_with_key]:
            c = deepcopy(config)
            for case in [50, None]:  # these raise TypeError from determine_config_layout
                c["tabs"] = case
                with pytest.raises(TypeError):
                    validators.validate_all(c)

    def test_tabs_len_0(self, config_multiple, config_single_with_key):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for config in [config_multiple, config_single_with_key]:
            c = deepcopy(config)
            for case in [[], tuple([])]:
                c["tabs"] = case
                validate_iteration_fail(c, "<lambda>", case)

    def test_unexpected_top_level_key(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        c["astring"] = "astring"
        validate_schema_fail(c, ["schema.SchemaWrongKeyError: Wrong key"])


# TEST CLASSES: TABS
# NONBREAKING, THEN BREAKING


@pytest.mark.function
@pytest.mark.run(order=2)
class TestSchemaTabs:
    """Does non-breaking tests for schemas with tabs"""

    def test_tab_header_input_present(self, config_multiple):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_multiple)
        for tab in c["tabs"]:
            if not tab.get("tab_header_input", None):
                raise AssertionError

    def test_tab_header_descriptions_absent(self, config_multiple):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for key in ["tab_header_description", "tab_header_long_description"]:
            c = deepcopy(config_multiple)
            c["tabs"][0] = del_key_if_present(c["tabs"][0], key)
            error_messages = []
            error_messages = validators._validate_schema(error_messages, c)
            if error_messages:
                raise AssertionError(key)

    def test_tab_header_descriptions_values_incl_none(self, config_multiple):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for key in ["tab_header_description", "tab_header_long_description"]:
            for case in [None, "astring", 1000, 2.5, KeyError]:  # unlikely to pass a class, but it should work
                c = deepcopy(config_multiple)
                c["tabs"][0][key] = case
                error_messages = []
                error_messages = validators._validate_schema(error_messages, c)
                if error_messages:
                    raise AssertionError(key, case)

    def test_headers_absent_in_single(self, config_single_with_key):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for key in ["tab_header_input", "tab_header_description", "tab_header_long_description"]:
            c = deepcopy(config_single_with_key)
            if c["tabs"][0].get(key, None):
                raise AssertionError(key)

    def test_items_present_and_iterable(self, config_multiple, config_single_with_key):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for config in [config_multiple, config_single_with_key]:
            for tab in config["tabs"]:
                if not tab.get("items", None):
                    raise AssertionError
                if not isinstance(tab["items"], list) and not isinstance(tab["items"], tuple):
                    raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=3)
class TestBreakingSchemasTabs:
    """Tests tabs item in schemas to ensure they break appropriately"""

    def test_tab_header_input_absent(self, config_multiple):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_multiple)
        c["tabs"][0] = del_key_if_present(c["tabs"][0], "tab_header_input")
        validate_schema_fail(c, ["tab#0: schema.SchemaMissingKeyError: Missing key: 'tab_header_input'"])

    def test_forbidden_headers_present(self, config_single_with_key):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for key in ["tab_header_input", "tab_header_description", "tab_header_long_description"]:
            c = deepcopy(config_single_with_key)
            c["tabs"][0][key] = "astring"
            validate_schema_fail(c, ["Forbidden"])

    def test_unexpected_headers_present(self, config_multiple, config_single_with_key):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for config in [config_multiple, config_single_with_key]:
            c = deepcopy(config)
            c["tabs"][0]["astring"] = "astring"
            validate_schema_fail(c, ["schema.SchemaWrongKeyError: Wrong key"])

    def test_headers_empty_string_len_0(self, config_multiple):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_multiple)
        for key in ["tab_header_input", "tab_header_description", "tab_header_long_description"]:
            c["tabs"][0][key] = ""
            validate_schema_fail(c, ["<lambda>"], key)

    def test_items_absent(self, config_multiple, config_single_with_key):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for config in [config_multiple, config_single_with_key]:
            c = deepcopy(config)
            c["tabs"][0] = del_key_if_present(c["tabs"][0], "items")
            # iteration fail because can't iterate over items if it's not there
            validate_iteration_fail(c, "schema.SchemaMissingKeyError: Missing key:")

    def test_wrong_type_items_not_iterable(self, config_multiple, config_single_with_key):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for config in [config_multiple, config_single_with_key]:
            c = deepcopy(config)
            for case in [{0, 1}, {0: 1}]:
                c["tabs"][0]["items"] = case
                validate_iteration_fail(c, "No further introspection possible", repr(case))

    def test_wrong_type_items_string(self, config_multiple, config_single_with_key):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for config in [config_multiple, config_single_with_key]:
            c = deepcopy(config)
            for case in ["string"]:
                c["tabs"][0]["items"] = case
                validate_iteration_fail(
                    c, "TypeError: string indices must be integers. No further introspection possible.", case
                )

    def test_wrong_type_items_other(self, config_multiple, config_single_with_key):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for config in [config_multiple, config_single_with_key]:
            c = deepcopy(config)
            for case in [50, None]:
                c["tabs"][0]["items"] = case
                validate_iteration_fail(c, "No further introspection possible", case)


# TEST CLASSES: ITEMS
# NONBREAKING, THEN BREAKING


@pytest.mark.function
@pytest.mark.run(order=2)
class TestSchemaItems:
    """Does non-breaking tests for items"""

    def test_mandatory_keys_present(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        config_layout = validators._determine_config_layout(config_all)
        if config_layout.find("without") != -1:
            items = c["items"]
        else:
            items = c["tabs"][0]["items"]
        for item in items:
            for key in ["item_choice_displayed", "item_inputs", "item_returns"]:
                if not item.get(key, None):
                    raise AssertionError

    def test_several_types_3_keys(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for key in ["item_choice_displayed", "item_description", "item_returns"]:
            for value in ["astring", 50, 2.57]:
                c = deepcopy(config_all)
                config_layout = validators._determine_config_layout(config_all)
                if config_layout.find("without") == -1:
                    c["tabs"][0]["items"][0][key] = value
                else:
                    c["items"][0][key] = value
                error_messages = []
                error_messages = validators._validate_schema(error_messages, c)
                if error_messages:
                    raise AssertionError

    def test_item_description_absent(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        config_layout = validators._determine_config_layout(config_all)
        if config_layout.find("without") == -1:
            c["tabs"][0]["items"][0] = del_key_if_present(c["tabs"][0]["items"][0], "item_description")
        else:
            c["items"][0] = del_key_if_present(c["items"][0], "item_description")
        error_messages = []
        error_messages = validators._validate_schema(error_messages, c)
        if error_messages:
            raise AssertionError

    def test_item_description_values(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for value in [None, ["astring"], ("string1", "string2")]:
            c = deepcopy(config_all)
            config_layout = validators._determine_config_layout(config_all)
            if config_layout.find("without") == -1:
                c["tabs"][0]["items"][0]["item_description"] = value
            else:
                c["items"][0]["item_description"] = value
            error_messages = []
            error_messages = validators._validate_schema(error_messages, c)
            if error_messages:
                raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=3)
class TestBreakingSchemasItems:
    """Tests items in schemas to ensure they break appropriately"""

    def test_3_required_keys_absent(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for case in ["item_choice_displayed", "item_inputs", "item_returns"]:
            c = deepcopy(config_all)
            config_layout = validators._determine_config_layout(config_all)
            if config_layout.find("without") == -1:
                c["tabs"][0]["items"][0] = del_key_if_present(c["tabs"][0]["items"][0], case)
            else:
                c["items"][0] = del_key_if_present(c["items"][0], case)
                validate_iteration_fail(c, "schema.SchemaMissingKeyError: Missing key: ", case)

    def test_2_keys_none_or_len_0(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for key in ["item_choice_displayed", "item_returns"]:
            for value in [None, ""]:
                case = "{}_{}".format(key, value)
                c = deepcopy(config_all)
                config_layout = validators._determine_config_layout(config_all)
                if config_layout.find("without") == -1:
                    c["tabs"][0]["items"][0][key] = value
                else:
                    c["items"][0][key] = value
                validate_schema_fail(c, ["item#0: schema.SchemaError: Key ", "<lambda>"], case)

    def test_item_description_len_0(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        config_layout = validators._determine_config_layout(config_all)
        if config_layout.find("without") == -1:
            c["tabs"][0]["items"][0]["item_description"] = ""
        else:
            c["items"][0]["item_description"] = ""
            validate_schema_fail(c, ["item#0: schema.SchemaError: Key ", "<lambda"])

    def test_item_inputs_wrong_types(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for case in [None, 50]:
            c = deepcopy(config_all)
            config_layout = validators._determine_config_layout(config_all)
            if config_layout.find("without") == -1:
                c["tabs"][0]["items"][0]["item_inputs"] = case
            else:
                c["items"][0]["item_inputs"] = case
            validate_iteration_fail(c, "WHILE ITERATING", case)

    def test_item_inputs_wrong_typestring(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        case = "asrting"
        c = deepcopy(config_all)
        config_layout = validators._determine_config_layout(config_all)
        if config_layout.find("without") == -1:
            c["tabs"][0]["items"][0]["item_inputs"] = case
        else:
            c["items"][0]["item_inputs"] = case
        validate_schema_fail(c, ["should be instance of"], case)

    def test_item_inputs_len_0(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for case in [[], tuple([])]:
            c = deepcopy(config_all)
            config_layout = validators._determine_config_layout(config_all)
            if config_layout.find("without") == -1:
                c["tabs"][0]["items"][0]["item_inputs"] = case
            else:
                c["items"][0]["item_inputs"] = case
            validate_schema_fail(c, ["lambda"], case)

    def unexpected_key_present(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        c = deepcopy(config_all)
        config_layout = validators._determine_config_layout(config_all)
        if config_layout.find("without") == -1:
            c["tabs"][0]["items"][0]["disallowedkey"] = "astring"
        else:
            c["items"][0]["disallowedkey"] = "astring"
        validate_schema_fail(c, ["item#0: schema.SchemaWrongKeyError: Wrong key"])


# TEST CLASSES: VALID_ENTRIES
# BREAKING ONLY

# self.entry_schema = Schema(lambda x: x is not None and len(str(x)) > 0)


@pytest.mark.breaking
@pytest.mark.run(order=3)
class TestBreakingSchemasValidEntries:
    """Tests item_inputs item in schemas to ensure they break appropriately"""

    def test_item_inputs_none_or_len_0(self, config_all):
        _ = self.__class__  # just to get rid of codacy warning, I know, it's stupid
        for value in [None, ""]:
            c = deepcopy(config_all)
            config_layout = validators._determine_config_layout(config_all)
            if config_layout.find("without") == -1:
                c["tabs"][0]["items"][0]["item_inputs"][0] = value
            else:
                c["items"][0]["item_inputs"][0] = value
                validate_iteration_fail(c, "<lambda>", value)


@pytest.mark.function
@pytest.mark.run(order=1)
def test_fn__config_tabs(config_all):
    """Hard to make this non tautological"""
    tabs = validators._config_tabs(config_all)
    if not isinstance(tabs[0]["items"], list):
        raise AssertionError()


# REPEAT VALUES TESTS #


@pytest.mark.function
@pytest.mark.run(order=2)
def test_fn__validate_no_return_value_overlap(config_all):
    """Expect pass on valid input data"""
    error_messages = []
    error_messages = validators._validate_no_return_value_overlap(error_messages, config_all)
    if error_messages:
        raise AssertionError


@pytest.mark.function
@pytest.mark.run(order=2)
def test_fn__validate_no_input_value_overlap(config_all):
    """Expect pass on valid input data"""
    error_messages = []
    error_messages = validators._validate_no_input_value_overlap(error_messages, config_all)
    if error_messages:
        raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=3)
def test_validate_no_return_value_overlap_fail(config_all_with_id):
    """Add a duplicate return value in a tab. Case sensitivity does not apply to return values"""
    conf, id_ = config_all_with_id
    c = deepcopy(conf)
    if id_.find("without") == -1:
        c["tabs"][0]["items"] += [c["tabs"][0]["items"][-1]]
    else:
        c["items"] += [c["items"][-1]]
    error_messages = []
    error_messages = validators._validate_no_return_value_overlap(error_messages, c)
    if all([x.find("there are repeated return values") == -1 for x in error_messages]):
        raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=3)
def test_validate_no_input_value_overlap_fail_within_an_item(config_all_with_id, random_string):
    """Add a duplicate valid_input value within an item. Tests both case sensitive and insensitive"""
    conf, id_ = config_all_with_id
    for case_sens in [True, False]:
        c = deepcopy(conf)
        c["case_sensitive"] = case_sens
        if case_sens:
            new_returns = [random_string, random_string]
        else:
            new_returns = [random_string, random_string.lower()]
        if id_.find("without") == -1:
            c["tabs"][0]["items"][0]["item_inputs"] += new_returns
        else:
            c["items"][0]["item_inputs"] += new_returns
        error_messages = []
        validators._validate_no_input_value_overlap(error_messages, c)
        if all([x.find("there are repeated input values") == -1 for x in error_messages]):
            raise AssertionError


@pytest.mark.breaking
@pytest.mark.run(order=3)
def test__validate_no_input_value_overlap_fail_between_item_and_tab(config_multiple, random_string):
    """Makes one tab header value equal to another's return value, both case sensitive and insensitive"""
    for case_sens in [True, False]:
        c = deepcopy(config_multiple)
        c["case_sensitive"] = case_sens
        c["tabs"][0]["tab_header_input"] = random_string
        if case_sens:
            c["tabs"][1]["items"][0]["item_inputs"] += [random_string]
        else:
            c["tabs"][1]["items"][0]["item_inputs"] += [random_string.lower()]
        error_messages = []
        validators._validate_no_input_value_overlap(error_messages, c)
        if all([x.find("there are repeated input values") == -1 for x in error_messages]):
            raise AssertionError


@pytest.mark.integration
@pytest.mark.run(order=4)
def test_fn_validate_all(config_all):
    """Ensures each test case overall validation passes before making them fail for different reasons"""
    validators.validate_all(config_all)


@pytest.mark.integration
@pytest.mark.run(order=4)
def test_fn_validate_all_fail(config_all):
    """Ensures each test case overall validation passes before making them fail for different reasons"""
    c = deepcopy(config_all)
    c[
        "unrecognized_key"
    ] = "astring"  # this particular error will cause the error message to be shortened, testing that function
    with pytest.raises(validators.InvalidInputError):
        validators.validate_all(c)


# MISC TESTS


@pytest.mark.function
@pytest.mark.run(order=1)
def test__shorten_long_schema_error_messages():
    """Tests that function"""
    error_messages = ["stuff that comes at the beginning in {'key': 'value'}"]
    error_messages = validators._shorten_long_schema_error_messages(error_messages)
    if error_messages[0] != "stuff that comes at the beginning in config":
        raise AssertionError
