#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Note that all formatting functions require a config that has gone through normalizer.normalize()"""

from __future__ import absolute_import, division, print_function, unicode_literals

from copy import deepcopy

import pytest

import tabbedshellmenus.formatting as formatting
import tabbedshellmenus.normalizer as normalizer


@pytest.mark.regression
@pytest.mark.run(order=2)
def test_regress__format_headers(data_regression, input_config_multiple_only):
    """Only multiple-type schema has headers; no need to normalize"""
    tab_num = 1  # minimum non-first ordinal of a multiple tab layout
    c = deepcopy(input_config_multiple_only)
    result = formatting._format_headers(c["tabs"], tab_num, 80)
    data = {"data": result}
    data_regression.check(data)


@pytest.mark.regression
@pytest.mark.run(order=3)
def test_regress__format_menu(data_regression, input_config_dict_and_id):
    """Only normalize single without key"""
    config, id_ = input_config_dict_and_id
    c = deepcopy(config)
    if id_.find("multiple") != -1:
        tab_num = 1
    else:
        tab_num = 0
        if id_.find("without") != -1:
            c = normalizer.normalize(c)
    result = formatting.format_menu(c, tab_num, 80).split("\n")
    data = {"data": result}
    data_regression.check(data)
