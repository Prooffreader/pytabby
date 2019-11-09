#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests pytabby/tab.py

Note that tabs depend on having normalized config input.
Regression tests only, based on input config
If input config changes, regression tests will have to change.
Functionality of this module is tested in menu.py tests
"""

# pylint: disable=C0116,C0330,W0212,C0103

from copy import deepcopy

import pytest

import pytabby.normalizer as normalizer
import pytabby.tab as tab


def freeze_tab(tab_dict):
    """Makes a reproducible version of tab_dict for regression testing"""
    lst = [":HEADS:"]
    for k in ["head_choice", "head_desc", "head_desc_long"]:
        lst.append(tab_dict[k])
    lst.append(":SELECTORS:")
    for item in tab_dict["selectors"]:
        lst.append(item)
    keys = sorted(tab_dict["input2result"].keys(), key=str)
    for k in keys:
        lst.append(":INPUT2RESULT:")
        lst.append(k)
        result = tab_dict["input2result"][k]
        lst.append(result["type"])
        lst.append(result.get("new_number", "n/a"))
        lst.append(result.get("return_value", "n/a"))
    return lst


@pytest.mark.regression
@pytest.mark.run(order=3)
def test_regress_create_tab_object(data_regression, config_all_with_id):
    """Only normalize single without key"""
    config, id_ = config_all_with_id
    c = deepcopy(config)
    if id_.find("without") != -1:
        c = normalizer.normalize(c)
    tabs = tab.create_tab_objects(c)
    data = {}
    for i, tab_instance in enumerate(tabs):
        data[i] = freeze_tab(tab_instance.__dict__)
    data_regression.check(data)
