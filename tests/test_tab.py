#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Note that tabs depend on having normalized config input."""

# pylama:ignore=W293,W291,W391,E302,E128,E127,E303,E501 (will be fixed by black)

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

from copy import deepcopy

import pytest

import tabbedshellmenus.normalizer as normalizer
import tabbedshellmenus.tab as tab


def freeze_tab(tab_dict):
    lst = [":HEADS:"]
    for k in ["head_choice", "head_desc", "head_desc_long"]:
        lst.append(tab_dict[k])
    lst.append(":SELECTORS:")
    for item in tab_dict["selectors"]:
        lst.append(item)
    keys = sorted(tab_dict["input2result"].keys(), key=lambda x: str(x))
    # TODO: ^ shouldn't they already be strings if they've been normalized?
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
def test_regress_create_tab_object(data_regression, input_config_dict_and_id):
    """Only normalize single without key"""
    config, id_ = input_config_dict_and_id
    c = deepcopy(config)
    if id_.find("without") != -1:
        c = normalizer.normalize(c)
    tabs = tab.create_tab_objects(c)
    data = {}
    for i, tab_instance in enumerate(tabs):
        data[i] = freeze_tab(tab_instance.__dict__)
    data_regression.check(data)
