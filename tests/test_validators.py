#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

import pysimpletabshellmenu.validators as validators


def test__determine_schema_type(input_config_dict_and_id):
    """As long as naming convention of test files stated in <root>/tests/data are followed, this should
    pass, and that was tested in conftest.py
    """
    config, id_ = input_config_dict_and_id
    print(id_)
    schema_type = validators._determine_schema_type(config)
    assert schema_type in ("multiple", "single_with_key", "single_without_key")
    assert 1 == 1
    if schema_type == "multiple":
        assert id_.find("multiple") != -1
    if schema_type.startswith("single"):
        assert id_.find("single") != -1
        if schema_type.endswith("_with_key"):
            assert id_.find("with_key") != -1
        if schema_type.endswith("_without_key"):
            assert id_.find("without_key") != -1




    # """Determines which of three valid schema types applies to input dict.
    # Used in validate_schema()

    # Valid Types are:
    # 1. multiple tabs ('multiple')
    # 2. single tab with tab key ('single_with_key')
    # 3. single tab without tab key ('single_without_key')
    # note that single tabs should have no header-related keys; this is checked in the Schema portion

    # :param dict_: A dict
    # :type dict: dict
    # :returns: type of schema
    # :rtype: str

    # """
    # if "tabs" in dict_.keys():
    #     if len(dict["tabs"] > 1):
    #         schema_type = "multiple"
    #     else:
    #         schema_type = "single_with_key"
    # else:
    #     schema_type = "single_without_key"
    # return schema_type