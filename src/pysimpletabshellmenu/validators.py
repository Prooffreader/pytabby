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


def validate_input_overlaps():
    pass
