#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests src/menu.py

NOTE: As it is needed there to create a pytest fixture, the static method Menu.safe_read_yaml() is tested in
conftest.py instead of here.
"""

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import


def sort_dict_to_list(d):
    """In order to make regression tests work in Python <3.6"""
    keys = sorted(d.keys(), key=lambda x: str(x))
    new_list = []
    for k in keys:
        value = d[k]
        if isinstance(value, dict):
            value = sort_dict_to_list(value)
        elif isinstance(value, list):
            value.sort()
        new_list.append([k, value])
    return new_list
