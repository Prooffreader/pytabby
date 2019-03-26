#!/usr/bin/env python
# -*- coding: utf-8 -*-pass

"""Functions to validate inputs and configs"""

from schema import Schema, Or, Optional


class _ValidSchemas:
    """Data-holding class for different schema.Schema instances to use in dict validation. Used in validate_schema()"""

    def __init__(self):
        self.with_key_outer_schema = Schema(
            {"case_sensitive": bool, Optional("screen_width"): int, "tabs": list}
        )

        self.without_key_outer_schema = Schema(
            {"case_sensitive": bool, Optional("screen_width"): int, "items": list}
        )

        self.multiple_tab_schema = Schema(
            {
                "header_choice_displayed_and_accepted": Or(int, str),
                "header_description": Or(str, None),
                "items": list,
            }
        )

        self.single_tab_schema = Schema({"items": list})

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
    Used in validate_schema()

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


def validate_schema(dict_):
    """Validates that the yaml file or dict past to the Menu instance has the expected schema.

    Examples of valid schemas can be seen in the examples/ folder of the git repo, or in the docs.
    There are two kinds of schemas, one with headers (i.e. with multiple tabs) and one without headers (i.e.
    with only one tab, which may be omitted or may be present as a 'tab' key in the schema).

    :param dict_: A dict
    :type dict: dict
    :returns: None
    :raises: :class:`Schema.SchemaError`: if dict_ departs from valid schema
    """
    schema_type = _determine_schema_type(dict_)
    if schema_type == "multiple":
        _ = _ValidSchemas.with_key_outer_schema.validate(dict_)
        for tab in dict_["tabs"]:
            _ = _ValidSchemas.multiple_tab_schema.validate(tab)
            for item in tab["items"]:
                _ = _ValidSchemas.item_schema.validate(item)
                for entry in item["valid_entries"]:
                    _ = _ValidSchemas.entry_schema.validate(entry)
    elif schema_type == "single_with_key":
        _ = _ValidSchemas.with_key_outer_schema.validate(dict_)
        _ = _ValidSchemas.single_tab_schema.validate(dict_["tab"])
        assert len(dict_["tab"] == 1)
        for item in dict_["tab"][0]["items"]:
            _ = _ValidSchemas.item_schema.validate(item)
            for entry in item["valid_entries"]:
                _ = _ValidSchemas.entry_schema.validate(entry)
    elif schema_type == "single_without_key":
        _ = _ValidSchemas.without_key_outer_schema.validate(dict_)
        for item in dict_["items"]:
            _ = _ValidSchemas.item_schema.validate(item)
            for entry in item["valid_entries"]:
                _ = _ValidSchemas.entry_schema.validate(entry)
    else:
        raise ValueError(f"schema_type {schema_type} is invalid")


def validate_input_overlaps():
    pass
