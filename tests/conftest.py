#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup fixtures.

NOTE: this script tests static method menu.Menu.safe_read_yaml() instead of test_menu.py"""

import os
from pathlib import Path

import pytest
import yaml  # imported due to Menu class dependency

from pysimpletabshellmenu.menu import Menu


_ = yaml  # just to get rid of pyflakes warning


def yaml_paths():
    """Retrieves paths of input yaml config files used to instantiate the menu.Menu class from tests/data.
    The contents of this folder can be changed without breaking the test suite, as long as they are valid yaml
    with valid schemas.
    """
    path_to_here = Path(os.path.realpath(__file__))
    data_path = path_to_here.parent / 'data'
    yaml_paths = [str(x) for x in data_path.glob('*.yaml')]
    return yaml_paths


# precursor for next constants
YAML_PATHS = sorted([path for path in yaml_paths()])

# constants for input_config_dict fixture
YAML_IDS = [os.path.split(os.path.splitext(path)[0])[1] for path in YAML_PATHS]
TEST_CONFIGS = [Menu.safe_read_yaml(path) for path in YAML_PATHS]


def pretest_yaml_ids():
    """Make sure yaml files in /test/data follow naming convention in that folders' README."""
    for yaml_id in YAML_IDS:
        assert yaml_id.find('multiple') != -1 or yaml_id.find('single') != -1
        if yaml_id.find('single') != -1:
            assert yaml_id.find('with_key') != -1 or yaml_id.find('without_key') != -1


pretest_yaml_ids()
print('pretest_yaml_ids test passed')


def pretest_configs_are_dicts():
    """Sanity check, ensure we are passing dicts"""
    for config in TEST_CONFIGS:
        assert isinstance(config, dict)


pretest_configs_are_dicts()
print('pretest_configs_are_dicts passed')


@pytest.fixture(scope="session", params=TEST_CONFIGS, ids=YAML_IDS)
def input_config_dict(request):
    """Returns config dicts of all files in /tests/data to run tests on.
    Since they are session-scoped, they should not be changed by tests."""
    return request.param


@pytest.fixture(scope="function", params=TEST_CONFIGS, ids=YAML_IDS)
def input_config_dict_and_id(request):
    """To test validators._determine_schema_type"""
    return (request.param, YAML_IDS[request.param_index])
