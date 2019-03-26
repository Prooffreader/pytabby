#!/usr/bin/env python
# -*- coding: utf-8 -*-pass

"""Functions to validate inputs and configs"""

from schema import Schema, Or, Optional


class _ValidSchemas:
    """Data-holding class for different schema.Schema instances to use in dict validation. Used in schema_is_valid()"""

    def __init__(self):
        self.outer_schema_multiple_or_single_with_key = Schema(
            {"case_sensitive": bool, Optional("screen_width"): int, "tabs": list}
        )

        self.outer_schema_single_without_key = Schema(
            {"case_sensitive": bool, Optional("screen_width"): int, "items": list}
        )

        self.tab_schema_multiple = Schema(
            {"header_choice_displayed_and_accepted": Or(int, str), "header_description": Or(str, None), "items": list}
        )

        self.tab_schema_single = Schema({"items": list})

        self.item_schema = Schema(
            {
                "choice_displayed": Or(str, int),
                "choice_description": str,
                "valid_entries": list,
                "returns": Or(str, int),
            }
        )

        self.entry_schema = Schema(Or(int, str))


def _determine_schema_type(dict_):
    """Determines which of three valid schema types applies to input dict.
    Used in schema_is_valid()

    Valid Types are:
    1. multiple tabs ('multiple')
    2. single tab with tab key ('single_with_key')
    3. single tab without tab key ('single_without_key')
    note that single tabs should have no header-related keys; this is checked in the Schema portion

    :param dict_: A dict
    :type dict: dict
    :returns: type of schema
    :rtype: str

    """
    if "tabs" in dict_.keys():
        if len(dict_["tabs"]) > 1:
            schema_type = "multiple"
        else:
            schema_type = "single_with_key"
    else:
        schema_type = "single_without_key"
    return schema_type


def schema_is_valid(dict_):
    """Validates that the dict past to the Menu instance has the expected schema.

    Examples of valid schemas can be seen in the examples/ folder of the git repo, or in the docs.
    There are two kinds of schemas, one with headers (i.e. with multiple tabs) and one without headers (i.e.
    with only one tab, which may be omitted or may be present as a 'tabs' key in the schema).

    :param dict_: A dict
    :type dict: dict
    :returns: bool
    :raises: :class:`Schema.SchemaError`: or AssertionError if dict_ departs from valid schema
    """
    try:
        schema_type = _determine_schema_type(dict_)
        valid_schemas = _ValidSchemas()
        if schema_type == "multiple":
            _ = valid_schemas.outer_schema_multiple_or_single_with_key.validate(dict_)
            for tab in dict_["tabs"]:
                _ = valid_schemas.tab_schema_multiple.validate(tab)
                for item in tab["items"]:
                    _ = valid_schemas.item_schema.validate(item)
                    for entry in item["valid_entries"]:
                        _ = valid_schemas.entry_schema.validate(entry)
        elif schema_type == "single_with_key":
            _ = valid_schemas.outer_schema_multiple_or_single_with_key.validate(dict_)
            try:
                assert len(dict_["tabs"]) == 1
            except AssertionError:
                raise Schema.SchemaError
            _ = valid_schemas.tab_schema_single.validate(dict_["tabs"][0])
            for item in dict_["tabs"][0]["items"]:
                _ = valid_schemas.item_schema.validate(item)
                for entry in item["valid_entries"]:
                    _ = valid_schemas.entry_schema.validate(entry)
        elif schema_type == "single_without_key":
            _ = valid_schemas.outer_schema_single_without_key.validate(dict_)
            for item in dict_["items"]:
                _ = valid_schemas.item_schema.validate(item)
                for entry in item["valid_entries"]:
                    _ = valid_schemas.entry_schema.validate(entry)
        else:
            raise ValueError(f"schema_type {schema_type} is invalid")
        return True
    except Exception as e:
        if str(e.__class__).find("Schema") != -1:
            return False
        else:
            raise e


def _find_tabs(dict_):
    """Finds (or creates) 'tabs' list from config dict for following tests

    :param dict_: config dict passed to Menu constructor
    :type dict_: dict
    :returns: list under 'tabs' key, explicit or implied
    'rtype': list
    """
    schema_type = _determine_schema_type(dict_)
    if schema_type == 'single_without_tabs':
        return [dict_['items']] # wrapped in a list as if there were tabs specified
    else:    
        return dict_['tabs']


def check_return_value_overlap(dict_):
    """Validates that all return values in every tab are unique. In theory, this could be possible but since
    multiple inputs are allowed for each menu item, in practice it is probably a mistake.
    
    :param dict_: config dict passed to Menu constructor
    :type dict_: dict
    :returns: None if valid config insofar as no return values overlap for any tab
    :raises: AssertionError if return values overlap, giving tab (if multiple) and values
    """
    try:
        tabs = _find_tabs(dict_)
        for tab in tabs:
            returns = [x['returns'] for x in tab['items']]
            assert len(returns) == len(set(returns))
    except AssertionError:
        if 'header_choice_displayed_and_accepted' in tab.keys():
            raise AssertionError(f'in tab {tab["header_choice_displayed_and_accepted"]}, there are repeated '
                                 f'return values: {returns}')
        else:
            raise AssertionError(f'in the single tab, there are repeated return values: {returns}')


def no_accepted_input_overlap(dict_):
    """Validates that the potential inputs on each tab are unambiguous, i.e. that any entry will either lead
    to another tab OR to returning a unique value OR the current tab's input value (this could have gone either
    way, I chose not to accept duplicate tab name and input in that tab)
    
    :param dict_: config dict passed to Menu constructor
    :type dict_: dict
    :returns: None if valid config insofar as no input values overlap for any tab
    :raises: AssertionError if input values overlap, giving tab (if multiple) and values
    """
    try:
        tabs = _find_tabs(dict_)
        tab_values = [x.get('header_choice_displayed_and_accepted', None) for x in tabs]
        tab_values = [x for x in tabs if x is not None]
        for tab in tabs:
            input_values = tab_values[:]
            for item in tab['items']:
                input_values += item['valid_entries']
                assert len(input_values) == len(set(input_values))
    except AssertionError:
        if 'header_choice_displayed_and_accepted' in tab.keys():
            raise AssertionError(f'in tab {tab["header_choice_displayed_and_accepted"]}, there are repeated '
                                 f'input values: {input values}, including other tabs')
        else:
            raise AssertionError(f'in the single tab, there are repeated input values: {input_values}')
