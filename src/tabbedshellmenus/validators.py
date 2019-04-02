#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions to validate inputs and configs"""

# pylama:ignore=W293,W291,W391,E302,E128,E127 (will be fixed by black)

from schema import Schema, Or, Optional, And


class ValueOverlapError(ValueError):
    pass


class _ValidSchemas:
    """Data-holding class for different schema.Schema instances to use in dict validation. Used in validate_schema()"""

    def __init__(self):
        self.outer_schema_multiple_or_single_with_key = Schema(
            {Optional("case_sensitive"): bool, Optional("screen_width"): int, "tabs": And(list, lambda x: len(x) > 0)}
        )

        self.outer_schema_single_without_key = Schema(
            {"case_sensitive": bool, Optional("screen_width"): int, "items": And(list, lambda x: len(x) > 0)}
        )

        self.tab_schema_multiple = Schema(
            {
                "header_choice_displayed_and_accepted": And(Or(int, str), lambda x: len(str(x)) > 0),
                "header_description": And(Or(str, None), lambda x: x is None or len(x) > 0),
                Optional("long_description"): And(str, lambda x: len(x) > 0),
                "items": And(list, lambda x: len(x) > 0),
            }
        )

        self.tab_schema_single = Schema({"items": And(list, lambda x: len(x) > 0)})

        self.item_schema = Schema(
            {
                "choice_displayed": And(Or(int, str), lambda x: len(str(x)) > 0),
                "choice_description": And(str, lambda x: len(x) > 0),
                "valid_entries": And(list, lambda x: len(x) > 0),
                "returns": And(Or(int, str), lambda x: len(str(x)) > 0),
            }
        )

        self.entry_schema = Schema(And(Or(int, str), lambda x: len(str(x)) > 0))


def _determine_schema_type(config):
    """Determines which of three valid schema types applies to input dict.
    Used in validate_schema()

    Valid Types are:
    1. multiple tabs ('multiple')
    2. single tab with tab key ('single_with_key')
    3. single tab without tab key ('single_without_key')
    note that single tabs should have no header-related keys; this is checked in the Schema portion

    :param config: A dict
    :type dict: dict
    :returns: type of schema
    :rtype: str

    """
    if "tabs" in config.keys():
        if len(config["tabs"]) > 1:
            schema_type = "multiple"
        else:
            schema_type = "single_with_key"
    else:
        schema_type = "single_without_key"
    return schema_type


def validate_schema(config):  # noqa: C901
    """Validates that the dict passed to the Menu instance has the expected schema.

    Examples of valid schemas can be seen in the examples/ folder of the git repo, or in the docs.
    There are two kinds of schemas, one with headers (i.e. with multiple tabs) and one without headers (i.e.
    with only one tab, which may be omitted or may be present as a 'tabs' key in the schema).

    :param config: config dict past from menu.Menu instance
    :type dict: dict
    :returns: None
    :raises: :class:`schema:SchemaError` if config departs from valid schema
    """
    try:
        schema_type = _determine_schema_type(config)
        valid_schemas = _ValidSchemas()
        if schema_type == "multiple":
            _ = valid_schemas.outer_schema_multiple_or_single_with_key.validate(config)
            for tab in config["tabs"]:
                _ = valid_schemas.tab_schema_multiple.validate(tab)
                for item in tab["items"]:
                    _ = valid_schemas.item_schema.validate(item)
                    for entry in item["valid_entries"]:
                        _ = valid_schemas.entry_schema.validate(entry)
        elif schema_type == "single_with_key":
            _ = valid_schemas.outer_schema_multiple_or_single_with_key.validate(config)
            try:
                assert len(config["tabs"]) == 1
            except AssertionError:
                raise Schema.SchemaError
            _ = valid_schemas.tab_schema_single.validate(config["tabs"][0])
            for item in config["tabs"][0]["items"]:
                _ = valid_schemas.item_schema.validate(item)
                for entry in item["valid_entries"]:
                    _ = valid_schemas.entry_schema.validate(entry)
        elif schema_type == "single_without_key":
            _ = valid_schemas.outer_schema_single_without_key.validate(config)
            for item in config["items"]:
                _ = valid_schemas.item_schema.validate(item)
                for entry in item["valid_entries"]:
                    _ = valid_schemas.entry_schema.validate(entry)
        else:
            raise ValueError(f"schema_type {schema_type} is invalid")
    except Exception as e:
        raise e


def _config_tabs(config):
    """Finds (or creates) 'tabs' list from config dict for following tests

    :param config: config dict passed to Menu constructor
    :type config: dict
    :returns: list under 'tabs' key, explicit or implied
    'rtype': list
    """
    schema_type = _determine_schema_type(config)
    if schema_type == "single_without_key":
        config["tabs"] = [{}]
        config["tabs"][0]["items"] = config["items"]
    return config["tabs"]


def validate_no_return_value_overlap(config):
    """Validates that all return values in every tab are unique.

    NOTE: Raises exception at first discovered tab with return value overlap, does not continue checking
    
    :param config: config dict passed to Menu constructor
    :type config: dict
    :returns: None
    :raises: :class:`ValueOverlapError` if return values overlap, giving tab (if applicable) and values
    """
    try:
        tabs = _config_tabs(config)
        for tab in tabs:
            returns = [x["returns"] for x in tab["items"]]
            assert len(returns) == len(set(returns))
    except AssertionError:
        if "header_choice_displayed_and_accepted" in tab.keys():
            raise ValueOverlapError(
                f'in tab {tab["header_choice_displayed_and_accepted"]}, there are repeated '
                + f"return values: {returns}"
            )
        else:
            raise ValueOverlapError(f"in the single tab, there are repeated return values: {returns}")


def validate_no_input_value_overlap(config):
    """Validates that the potential inputs on each tab are unambiguous, i.e. that any entry will either lead
    to another tab OR to returning a unique value OR the current tab's input value (this could have gone either
    way, I chose not to accept duplicate tab name and input in that tab)

    NOTE: Raises exception at first tab found with overlapping inputs, does not continue checking
    
    :param config: config dict passed to Menu constructor
    :type config: dict
    :returns: None
    :raises: :class:`ValueOverlapError` if input values overlap, giving tab (if applicable) and values
    """
    try:
        case_sensitive = config.get("case_sensitive", False)
        tabs = _config_tabs(config)
        tab_values = []
        for tab in tabs:
            header_choice = tab.get("header_choice_displayed_and_accepted", None)
            if header_choice:
                if not case_sensitive:
                    header_choice = header_choice.lower()
                tab_values.append(header_choice)
        for tab in tabs:
            input_values = tab_values[:]
            for item in tab["items"]:
                valid_entries = item["valid_entries"]
                if not case_sensitive:
                    valid_entries = [x.lower() if isinstance(x, str) else x for x in valid_entries]
                input_values += valid_entries
                assert len(input_values) == len(set(input_values))
    except AssertionError:
        if header_choice:
            raise ValueOverlapError(
                f"in tab {header_choice}, there are repeated input values: {sorted(input_values)},"
                + f"including other tabs. Note case_sensitive={case_sensitive}"
            )
        else:
            raise ValueOverlapError(
                f"in the single tab, there are repeated input values: {sorted(input_values)},"
                + f"Note case_sensitive={case_sensitive}"
            )


class InvalidInputError(Exception):
    pass


def validate_all(config):
    """Runs above non-underscored functions on input"""
    try:
        validate_schema(config)
        validate_no_input_value_overlap(config)
        validate_no_return_value_overlap(config)
    except Exception:
        raise InvalidInputError
