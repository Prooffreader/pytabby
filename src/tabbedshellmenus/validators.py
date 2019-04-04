#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions to validate inputs and configs. Note that this creates one exception listing all errors encountered"""

# pylama:ignore=W293,W291,W391,E302,E128,E305,E127,E303 (will be fixed by black)

from schema import Schema, Or, Optional, And, Forbidden

from collections import Counter


class InvalidInputError(ValueError):
    pass

error_messages = []  # will be mutated by functions


class _ValidSchemas:
    """Data-holding class for different schema.Schema instances to use in dict validation. Used in validate_schema()"""

    def __init__(self):
        self.outer_schema_multiple_or_single_with_key = Schema(
            {Optional("case_sensitive"): bool, 
             Optional("screen_width"): And(int, lambda x: x > 0), 
             "tabs": And(list, lambda x: len(x) > 0)}
        )

        self.outer_schema_single_without_key = Schema(
            {Optional("case_sensitive"): bool, 
             Optional("screen_width"): And(int, lambda x: x > 0), 
             "items": And(Or(list, tuple), lambda x: len(x) > 0)}
        )

        self.tab_schema_multiple = Schema(
            {
                "header_choice_displayed_and_accepted": lambda x: len(str(x)) > 0,
                Optional("header_description"): lambda x: (x or x is None) or len(str(x)) > 0,
                Optional("long_description"): lambda x: (x or x is None) or len(str(x)) > 0,
                "items": And(Or(list, tuple), lambda x: len(x) > 0),
            }
        )

        self.tab_schema_single_with_key = Schema(
            {
                Forbidden("header_choice_displayed_and_accepted"): object,
                Forbidden("header_description"): object,
                Forbidden("long_description"): object,
                "items": And(Or(list, tuple), lambda x: len(x) > 0)
            }
        )

        self.item_schema = Schema(
            {
                "choice_displayed": lambda x: x and len(str(x)) > 0,
                "choice_description": lambda x: x and len(str(x)) > 0,
                "valid_entries": And(Or(list, tuple), lambda x: len(x) > 0),
                "returns": lambda x: x and len(str(x)) > 0,
            }
        )

        self.entry_schema = Schema(lambda x: x and len(str(x)) > 0)

def _extract_class(class_repr):
    return class_repr.replace("<class '", "").replace("'>", "")

def  _validate_schema_part(error_messages, schema_, to_validate, prefix=None):
    """Mutates error_messages if error found"""
    try:
        _ = schema_.validate(to_validate)
    except Exception as e:
        error_type = _extract_class(str(e.__class__)) + ': '
        error_description = str(e).replace('\n', ' ')
        if not prefix:
            prefix = ''
        error_message = prefix + error_type + error_description
        error_messages.append(error_message)

def _determine_schema_type(config):
    """Determines which of three valid schema types applies to input dict.
    Used in validate_schema()

    Valid Types are:
    1. multiple tabs ('multiple')
    2. single tab with tab key ('single_with_key')
    3. single tab without tab key ('single_without_key')
    note that single tabs should have no header-related keys; this is checked in the Schema portion
    """
    if "tabs" in config.keys():
        if len(config["tabs"]) > 1:
            schema_type = "multiple"
        else:
            schema_type = "single_with_key"
    else:
        schema_type = "single_without_key"
    return schema_type


def validate_schema(error_messages, config):  # noqa: C901
    """Validates that the dict passed to the Menu instance has the expected schema. Mutates error_messages by
    appending all errors found

    Examples of valid schemas can be seen in the examples/ folder of the git repo, or in the docs.
    There are three kinds of schemas, one with multiple tabs, one with a single tab, and one with an implicit single
    tab that skips the redundant 'tabs' key
    """
    schema_type = _determine_schema_type(config)
    valid_schemas = _ValidSchemas()
    if schema_type == "multiple":
        _validate_schema_part(error_messages, valid_schemas.outer_schema_multiple_or_single_with_key, config)
        for tab_num, tab in enumerate(config["tabs"]):
            prefix = 'tab#{0}: '.format(tab_num)
            _validate_schema_part(error_messages, valid_schemas.tab_schema_multiple, tab, prefix)
            for item_num, item in enumerate(tab["items"]):
                prefix = 'tab#{0},item#{1}: '.format(tab_num, item_num)
                _validate_schema_part(error_messages, valid_schemas.item_schema, item, prefix)
                for entry_num, entry in enumerate(item["valid_entries"]):
                    prefix = 'tab#{0},item#{1},valid_entry#{2}: '.format(tab_num, item_num, entry_num)
                    _validate_schema_part(error_messages, valid_schemas.entry_schema, entry, prefix)
    elif schema_type == "single_with_key":
        _validate_schema_part(error_messages, valid_schemas.outer_schema_multiple_or_single_with_key, config)
        prefix = "sole tab: "
        _validate_schema_part(error_messages, valid_schemas.tab_schema_single_with_key, config["tabs"][0], prefix)
        for item_num, item in enumerate(config["tabs"][0]["items"]):
            prefix = "sole tab,item#{0}: ".format(item_num)
            _validate_schema_part(error_messages, valid_schemas.item_schema, item, prefix)
            for entry_num, entry in enumerate(item["valid_entries"]):
                prefix = 'sole tab,item#{0},valid_entry#{1}: '.format(item_num, entry_num)
                _validate_schema_part(error_messages, valid_schemas.entry_schema, entry, prefix)
    elif schema_type == "single_without_key":
        _validate_schema_part(error_messages, valid_schemas.outer_schema_single_without_key, config)
        for item_num, item in enumerate(config["items"]):
            prefix = "item#{0}: ".format(item_num)
            _validate_schema_part(error_messages, valid_schemas.item_schema, item, prefix)
            for entry_num, entry in enumerate(item["valid_entries"]):
                prefix = 'item#{0},valid_entry#{1}: '.format(item_num, entry_num)
                _validate_schema_part(error_messages, valid_schemas.entry_schema, entry, prefix)


def _config_tabs(config):
    """Finds (or creates) 'tabs' list from config dict for following tests.
    Creates one from top level 'items' if type is single_without_key
    """
    schema_type = _determine_schema_type(config)
    if schema_type == "single_without_key":
        config["tabs"] = [{}]
        config["tabs"][0]["items"] = config["items"]
    return config["tabs"]


def _count_for_overlap(items_):
    """counts items, returns multiple values only or empty set"""
    counter = Counter(items_)
    multiples = [x for x in counter.most_common() if x[1] > 1]
    return multiples





def validate_no_return_value_overlap(error_messages, config):
    """Validates that all return values in every tab are unique. Mutates error_messages with all errors found

    NOTE: Checks all tabs, so can result in long error message
    NOTE: Case insensitivity does not affect return values
    """
    tabs = _config_tabs(config)
    error_messages = []
    for tab_num, tab in enumerate(tabs):
        returns = [x["returns"] for x in tab["items"]]
        multiples = _count_for_overlap(returns)
        if multiples:
            if "header_choice_displayed_and_accepted" in tab.keys():
                error_messages.append(
                    "In tab#{0}, there are repeated return values: {1}.".format(
                        tab_num, multiples)
                )
            else:
                error_messages.append("In the single tab, there are repeated return values: {0}".format(multiples))


def validate_no_input_value_overlap(error_messages, config):
    """Validates that the potential inputs on each tab are unambiguous, i.e. that any entry will either lead
    to another tab OR to returning a unique value OR the current tab's input value (this could have gone either
    way, I chose not to accept duplicate tab name and input in that tab)

    NOTE: Mutates error_messages
    NOTE: Case sensitivity casts all inputs to lowercase, which can create overlap
    """
    case_sensitive = config.get('case_sensitive', False)
    schema_type = _determine_schema_type(config)
    tabs = _config_tabs(config)
    error_messages = []
    for tab_num, tab in enumerate(tabs):
        choices = []
        if schema_type == 'multiple':
            choices.append(tab["header_choice_displayed_and_accepted"])
        for item in tab['items']:
            for entry in item["valid_entries"]:
                choices.append(entry)
        if case_sensitive:
            choices = [choice.lower() for choice in choices]
        multiples = _count_for_overlap(choices)
        if multiples:
            if not config.get('case_sensitive', False):
                case_sensitive_message = (' Note case sensitive is false, so values have been changed to lower-case, '
                                        'which can create overlap')
            else:
                case_sensitive_message = ''
            if schema_type == 'multiple':
                error_messages.append(
                    "In tab#{0}, there are repeated input values including tab selectors: {1}.{2}".format(
                        tab_num, multiples, case_sensitive_message)
                )
            else:
                error_messages.append(
                    "In single tab, there are repeated input values: {0}.{1}".format(
                        multiples, case_sensitive_message)
                )


def validate_all(config):
    """Runs above non-underscored functions on input"""
    validate_schema(error_messages, config)
    validate_no_input_value_overlap(error_messages, config)
    validate_no_return_value_overlap(error_messages, config)
    if error_messages:
        printed_message = ["", "Errors:"]
        for i, message in enumerate(error_messages):
            printed_message.append("{0}. {1}".format(i, message))
        raise InvalidInputError('\n'.join(printed_message))
