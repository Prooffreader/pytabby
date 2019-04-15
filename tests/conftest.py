#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup fixtures.

NOTE: this script tests uses static method menu.Menu.safe_read_yaml() and function
validators._determine_schema_type, but they are both tested in their respective sections. So Exceptions will be
raised here before those tests run, redundantly, but they're in both places to ensure 100% coverage
 
TODO: Fix this
"""


from __future__ import absolute_import, division, print_function, unicode_literals

from copy import deepcopy
import os

import pytest

from tabbedshellmenus import Menu

pytest_plugins = ("regressions",)


def load_multiple_config_yaml():
    """Retrieves config dict from tests/data/test_config.yaml

    Tests whether it is multiple
    """
    path_to_here = os.path.realpath(__file__)
    this_dir = os.path.split(path_to_here)[0]
    config_path = os.path.join(this_dir, "data", "test_config.yaml")
    config = Menu.safe_read_yaml(config_path)
    assert len(config["tabs"]) > 1  # noqa
    if not isinstance(config, dict):
        raise AssertionError
    return config


def create_single_with_key(multiple_config):
    """Creates single_with_key type from multiple config"""
    d = deepcopy(multiple_config)
    d["tabs"] = d["tabs"][:1]
    del d["tabs"][0]["header_entry"]
    for key in ["header_description", "header_long_description"]:
        try:
            del d["tabs"][0][key]
        except KeyError:
            pass
    return d


def create_single_without_key(with_key):
    """Creates single_without_key type from single_with_key config"""
    d = deepcopy(with_key)
    d["items"] = d["tabs"][0]["items"]
    del d["tabs"]
    return d


@pytest.fixture(scope="function")
def config_multiple():
    """Returns multiple config fixture."""
    return load_multiple_config_yaml()


@pytest.fixture(scope="function")
def config_single_with_key():
    """Returns single with key config fixture."""
    multiple = load_multiple_config_yaml()
    return create_single_with_key(multiple)


@pytest.fixture(scope="function")
def config_single_without_key():
    """Returns single without key config fixture"""
    multiple = load_multiple_config_yaml()
    with_key = create_single_with_key(multiple)
    return create_single_without_key(with_key)


@pytest.fixture(
    scope="function",
    params=[
        load_multiple_config_yaml(),
        create_single_with_key(load_multiple_config_yaml()),
        create_single_without_key(create_single_with_key(load_multiple_config_yaml())),
    ],
    ids=["multiple", "single_with_key", "single_without_key"],
)
def config_all(request):
    """Returns all three config types"""
    return request.param


@pytest.fixture(
    scope="function",
    params=[
        load_multiple_config_yaml(),
        create_single_with_key(load_multiple_config_yaml()),
        create_single_without_key(create_single_with_key(load_multiple_config_yaml())),
    ],
    ids=["multiple", "single_with_key", "single_without_key"],
)
def config_all_with_id(request):
    """Returns tuple of config dict, id for all config types"""
    return (request.param, ["multiple", "single_with_key", "single_without_key"][request.param_index])


@pytest.fixture(scope="function")
def random_string():
    """Stringified urandom bytes with alphanumerics only and alternating upper and lower case alphabeticals"""
    astr = str(os.urandom(10))
    # capitalize every other alphabetic and remove non-alphanumeric
    n = 0
    new = []
    for char in astr:
        if char.isalpha():
            n += 1
            if n % 2 == 0:
                new.append(char.upper())
            else:
                new.append(char.lower())
        else:
            if char.isalnum():
                new.append(char)
    new.extend("aBc")  # just in case no alphas are included
    return "".join(new)
