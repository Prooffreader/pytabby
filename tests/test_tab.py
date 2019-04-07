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

def sort_dict_to_list(d):
    """In order to make regression tests work in Python <3.6"""
    keys = sorted(d.keys())
    new_list = []
    for k in keys:
        value = d[k]
        if isinstance(value, dict):
            value = sort_dict(value)
        elif isinstance(value, list):
            value.sort()
        new_list.append([k, value])
    return new_list


@pytest.mark.regression
@pytest.mark.run(order=3)
def test_regress_create_tab_object(data_regression, input_config_dict_and_id):
    """Only normalize single without key"""
    config, id_ = input_config_dict_and_id
    c = deepcopy(config)
    if id_.find('without') != -1:
        c = normalizer.normalize(c)
    tabs = tab.create_tab_objects(c)
    tab_dicts = [sort_dict_to_list(x.__dict__) for x in tabs]
    data = {'data': sorted(tab_dicts)}
    data_regression.check(data)
