#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions to validate config dict as passed to menu.Menu instantiator

Note that this module creates one exception listing all errors encountered. That way the user has the change to fix
all errors, instead of having to deal with exception after exception one at a time

Note on config_layout:
There are three possible values of config_layout, determined from the config dict
1. 'multiple': a config with multiple tabs, therefore by necessity having an outermost 'tabs' key
2. 'single_with_key': a config with a single tab (i.e. with no tabs), but also containing a redundant 'tabs' key
                      whose values is a list of size one containing a dict with the key 'items'
3. 'single_without_key': a config with a single tab but lacking the 'tabs' key; the single dict with the key 'items'
                         is at the top level of the config dict, i.e. where 'tabs' would have been
"""


import re
from collections import Counter

from schema import And, Forbidden, Optional, Or, Schema
from schema import (
    SchemaError,
    SchemaForbiddenKeyError,
    SchemaMissingKeyError,
    SchemaUnexpectedTypeError,
    SchemaWrongKeyError,
)

# SchemaOnlyOneAllowedError is not used

SCHEMA_ERRORS = (
    SchemaError,
    SchemaForbiddenKeyError,
    SchemaMissingKeyError,
    SchemaUnexpectedTypeError,
    SchemaWrongKeyError,
)


class InvalidInputError(Exception):
    """Catchall exception for invalid input.

    Prints list of all errors to stderr.
    """


class _ValidSchemas:
    """Data-holding class for Schema instances appropriate for different types of config.

    Instantiated from validate_schema() only
    """

    def __init__(self):

        # outermost keys of config if it has a 'tabs' outermost key, i.e. if it is of layout
        # multiple or single_with_key
        self.outer_schema_multiple_or_single_with_key = Schema(
            {
                Optional("case_sensitive"): bool,
                Optional("screen_width"): And(int, lambda x: x > 0),
                "tabs": And(Or(list, tuple), lambda x: len(x) > 0),
            }
        )

        # outermost keys for single_without_key layout
        self.outer_schema_single_without_key = Schema(
            {
                Optional("case_sensitive"): bool,
                Optional("screen_width"): And(int, lambda x: x > 0),
                "items": And(Or(list, tuple), lambda x: len(x) > 0),
            }
        )

        # schema for each 'tab' value if there are multiple tabs
        self.tab_schema_multiple = Schema(
            {
                "tab_header_input": lambda x: x is not None and len(str(x)) > 0,
                Optional("tab_header_description"): lambda x: x is None or len(str(x)) > 0,
                Optional("tab_header_long_description"): lambda x: x is None or len(str(x)) > 0,
                "items": And(Or(list, tuple), lambda x: len(x) > 0),
            }
        )

        # schema for the single redundant 'tab' value for the 'single_with_key' layout
        self.tab_schema_single_with_key = Schema(
            {
                Forbidden("tab_header_input"): object,
                Forbidden("tab_header_description"): object,
                Forbidden("tab_header_long_description"): object,
                "items": And(Or(list, tuple), lambda x: len(x) > 0),
            }
        )

        # schema for items
        self.item_schema = Schema(
            {
                "item_choice_displayed": lambda x: x is not None and len(str(x)) > 0,
                Optional("item_description"): lambda x: x is None or len(str(x)) > 0,
                "item_inputs": And(Or(list, tuple), lambda x: len(x) > 0),
                "item_returns": lambda x: x is not None and len(str(x)) > 0,
            }
        )

        # schema for each entry in 'item_inputs'
        self.entry_schema = Schema(lambda x: x is not None and len(str(x)) > 0)


def _extract_class(class_repr):
    """Helper function to prettify class specifications in error messages

    Example:
        >>> _extract_class("<class 'str'>)
        'str'

    Args:
        class_repr (str): the output of an instance's .__class__ attribute

    Returns
        str, shorter
    """
    return class_repr.replace("<class '", "").replace("'>", "")


def _validate_schema_part(error_messages, schema_, to_validate, prefix=None):
    """Validates that a section of the config follows schema

    Args:
        error_messages (list of str): list of all error messages produced by the validator to date
        schema_ (schema.Schema): instance defined in _ValidSchemas() class in this module
        to_validate (dict or str): config or subsection of config to validate
        prefix (str): prefix to be added to error message, to make it clear exactly where in the
                      config dict the error occurred

    Returns:
        (list of str) error_messages, extended if applicable
    """
    try:
        _ = schema_.validate(to_validate)
    except SCHEMA_ERRORS as e:  # noqa
        error_type = _extract_class(str(e.__class__)) + ": "
        error_description = str(e).replace("\n", " ")
        if not prefix:
            prefix = ""
        error_message = prefix + error_type + error_description
        error_messages.append(error_message)
    return error_messages


def _determine_config_layout(config):
    """Determines which of three valid schema types applies to input dict.

    Used in validate_schema()

    Valid Types are:
    1. multiple tabs ('multiple')
    2. single tab with tab key ('single_with_key')
    3. single tab without tab key ('single_without_key')
    note that single tabs should have no header-related keys; this is checked in the Schema portion

    This function does not do a lot of error-checking, that is left to other functions.
    """
    config_layout = None
    if "tabs" in config.keys():
        if len(config["tabs"]) > 1:
            config_layout = "multiple"
        else:
            config_layout = "single_with_key"
    else:
        config_layout = "single_without_key"
    return config_layout


def _validate_schema_multiple(error_messages, config, valid_schemas):
    """Called by _validate_schema() (q.v.) if multiple type"""
    error_messages = _validate_schema_part(
        error_messages, valid_schemas.outer_schema_multiple_or_single_with_key, config
    )
    try:
        level = "tabs"
        for tab_num, tab in enumerate(config["tabs"]):
            prefix = "tab#{0}: ".format(tab_num)
            error_messages = _validate_schema_part(error_messages, valid_schemas.tab_schema_multiple, tab, prefix)
            level = "items"
            for item_num, item in enumerate(tab["items"]):
                prefix = "tab#{0},item#{1}: ".format(tab_num, item_num)
                error_messages = _validate_schema_part(error_messages, valid_schemas.item_schema, item, prefix)
                level = "item_inputs"
                for entry_num, entry in enumerate(item["item_inputs"]):
                    prefix = "tab#{0},item#{1},valid_entry#{2}: ".format(tab_num, item_num, entry_num)
                    error_messages = _validate_schema_part(error_messages, valid_schemas.entry_schema, entry, prefix)
    except Exception as e:  # noqa
        error_messages = _catch_iteration_error(error_messages, e, level)
    return error_messages


def _validate_schema_single_with_key(error_messages, config, valid_schemas):
    """Called by _validate_schema() (q.v.) if single_with_tab type"""
    error_messages = _validate_schema_part(
        error_messages, valid_schemas.outer_schema_multiple_or_single_with_key, config
    )
    prefix = "sole tab: "
    try:
        level = "tabs"
        error_messages = _validate_schema_part(
            error_messages, valid_schemas.tab_schema_single_with_key, config["tabs"][0], prefix
        )
        level = "items"
        for item_num, item in enumerate(config["tabs"][0]["items"]):
            prefix = "sole tab,item#{0}: ".format(item_num)
            error_messages = _validate_schema_part(error_messages, valid_schemas.item_schema, item, prefix)
            level = "item_inputs"
            for entry_num, entry in enumerate(item["item_inputs"]):
                prefix = "sole tab,item#{0},valid_entry#{1}: ".format(item_num, entry_num)
                error_messages = _validate_schema_part(error_messages, valid_schemas.entry_schema, entry, prefix)
    except Exception as e:  # noqa
        error_messages = _catch_iteration_error(error_messages, e, level)
    return error_messages


def _validate_schema_single_without_key(error_messages, config, valid_schemas):
    """Called by _validate_schema() (q.v.) if single_without_tab type"""
    error_messages = _validate_schema_part(error_messages, valid_schemas.outer_schema_single_without_key, config)
    try:
        level = "items"
        for item_num, item in enumerate(config["items"]):
            prefix = "item#{0}: ".format(item_num)
            error_messages = _validate_schema_part(error_messages, valid_schemas.item_schema, item, prefix)
            level = "item_inputs"
            for entry_num, entry in enumerate(item["item_inputs"]):
                prefix = "item#{0},valid_entry#{1}: ".format(item_num, entry_num)
                error_messages = _validate_schema_part(error_messages, valid_schemas.entry_schema, entry, prefix)
    except Exception as e:  # noqa
        error_messages = _catch_iteration_error(error_messages, e, level)
    return error_messages


def _catch_iteration_error(error_messages, e, level):
    """Stops introspection on an iterable when it throws an exception, adds it to error_messages"""
    error_type = _extract_class(str(e.__class__)) + ": "
    error_description = str(e).replace("\n", " ")
    error_message = "WHILE ITERATING OVER {0}: {1}{2}. No further introspection possible.".format(
        level, error_type, error_description
    )
    error_messages.append(error_message)
    return error_messages


def _validate_schema(error_messages, config):
    """Validates that config has the expected schema.

    Examples of valid schemas can be seen in the examples/ folder of the git repo, or in the docs.
    There are three kinds of schemas, one with multiple tabs, one with a single tab, and one with an implicit single
    tab that skips the redundant 'tabs' key

    Args:
        error_messages: list of str passed around
        config: the dict

    Returns:
        error messages list of str
    """
    config_layout = _determine_config_layout(config)
    valid_schemas = _ValidSchemas()
    if config_layout == "multiple":
        error_messages = _validate_schema_multiple(error_messages, config, valid_schemas)
    elif config_layout == "single_with_key":
        error_messages = _validate_schema_single_with_key(error_messages, config, valid_schemas)
    elif config_layout == "single_without_key":
        error_messages = _validate_schema_single_without_key(error_messages, config, valid_schemas)
    else:
        raise AssertionError("unrecognized config_layout")
    return error_messages


def _config_tabs(config):
    """Returns 'tabs' list unless single_without_key, in which case it manufactures one"""
    config_layout = _determine_config_layout(config)
    if config_layout == "single_without_key":
        return [{"items": config["items"]}]
    return config["tabs"]


def _count_for_overlap(items_):
    """Counts items, returns multiple values only or empty set"""
    counter = Counter(items_)
    multiples = [x for x in counter.most_common() if x[1] > 1]
    return multiples


def _validate_no_return_value_overlap(error_messages, config):
    """Validates that all return values in every tab are unique.

    Checks all tabs, so can result in long error message
    Case insensitivity does not affect return values
    """
    tabs = _config_tabs(config)
    for tab_num, tab in enumerate(tabs):
        returns = []
        if "items" in tab.keys():  # so as not to raise premature KeyError in invalid schema
            for item in tab["items"]:
                value = item.get("item_returns", None)
                if value:  # so as not to raise premature KeyError in invalid schema
                    returns.append(value)
        multiples = _count_for_overlap(returns)
        if multiples:
            if "tab_header_input" in tab.keys():
                error_messages.append("In tab#{0}, there are repeated return values: {1}.".format(tab_num, multiples))
            else:
                error_messages.append("In the single tab, there are repeated return values: {0}".format(multiples))
    return error_messages


def _validate_no_input_value_overlap(error_messages, config):  # noqa:C901
    """Validates that the potential inputs on each tab are unambiguous.

    In other words, validates that any entry will either lead
    to another tab OR to returning a unique value OR the current tab's input value (this could have gone either
    way, I chose not to accept duplicate tab name and input in that tab for the sake of consistency rather than
    freeing up one possible input in a sort of weird edge case)

    Case insensitivity casts all inputs to lowercase, which can create overlap
    """
    case_sensitive = config.get("case_sensitive", False)
    config_layout = _determine_config_layout(config)
    tabs = _config_tabs(config)
    starting_choices = []
    # get tab header choices if multiple tabs
    if config_layout == "multiple":
        for tab in tabs:
            if tab.get("tab_header_input", None):  # so as not to raise premature KeyError for invalid schema
                starting_choices.append(tab["tab_header_input"])
    for tab_num, tab in enumerate(tabs):
        choices = starting_choices[:]
        if "items" in tab.keys():  # so as not to raise premature KeyError for invalid schema
            for item in tab["items"]:
                if "item_inputs" in item.keys():  # so as not to raise premature KeyError for invalid schema
                    for entry in item["item_inputs"]:
                        choices.append(entry)
            if not case_sensitive:
                choices = [str(choice).lower() for choice in choices]
        multiples = _count_for_overlap(choices)
        if multiples:
            if not case_sensitive:
                case_sensitive_message = (
                    " Note case sensitive is false, so values have been changed to lower-case, "
                    "which can create overlap"
                )
            else:
                case_sensitive_message = ""
            if config_layout == "multiple":
                error_messages.append(
                    "In tab#{0}, there are repeated input values including tab selectors: {1}.{2}".format(
                        tab_num, multiples, case_sensitive_message
                    )
                )
            else:
                error_messages.append(
                    "In single tab, there are repeated input values: {0}.{1}".format(
                        multiples, case_sensitive_message
                    )
                )
    return error_messages


def _shorten_long_schema_error_messages(error_messages):
    """The schema package puts the entire config in the error message; this function removes it."""
    for i, message in enumerate(error_messages[:]):
        if re.search("in {.+}$", message):
            error_messages[i] = re.sub(r"in \{.+\}$", "in config", message)
    return error_messages


def validate_all(config):
    """Runs above non-underscored functions on input"""
    error_messages = []
    error_messages = _validate_schema(error_messages, config)
    error_messages = _validate_no_input_value_overlap(error_messages, config)
    error_messages = _validate_no_return_value_overlap(error_messages, config)
    if error_messages:
        error_messages = _shorten_long_schema_error_messages(error_messages)
        printed_message = ["", "Errors:"]
        for i, message in enumerate(error_messages):
            printed_message.append("{0}. {1}".format(i + 1, message))
        raise InvalidInputError("\n".join(printed_message))
