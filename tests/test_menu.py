#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests menu.py"""

from __future__ import absolute_import, division, print_function, unicode_literals

from copy import deepcopy
import json
import os

import pytest

# import from __init__
from tabbedshellmenus import Menu
import tabbedshellmenus


def yaml_path():
    """Gets path to test yaml file"""
    path_to_here = os.path.realpath(__file__)
    this_dir = os.path.split(path_to_here)[0]
    return os.path.join(this_dir, "data", "test_config.yaml")


@pytest.mark.integration
@pytest.mark.run(order=-5)
class TestStaticMethods:
    """Tests the static methods to load data"""

    def test_yaml(self):
        """Loads test yaml and instantiates Menu"""
        config = Menu.safe_read_yaml(yaml_path())
        menu = Menu(config) #noqa

    def test_json(self, tmpdir):
        """Loads test yaml, converts to json, loads json and instantiates Menu

        Also asserts the two dicts are equal
        """
        config_from_yaml = Menu.safe_read_yaml(yaml_path())
        p = tmpdir.mkdir("tabbedshellmenustest").join("temp.json")
        p.write(json.dumps(config_from_yaml))
        config_from_json = Menu.read_json(str(p))
        if not config_from_yaml == config_from_json:
            raise AssertionError


@pytest.mark.function
@pytest.mark.run(order=6)
def test_method__change_tab(config_multiple, capsys, random_string):
    """Tests menu._change_tab"""
    c = deepcopy(config_multiple)
    c["tabs"][1]["header_entry"] = random_string[:3]
    c["tabs"][1]["header_description"] = random_string[3:7]
    c["tabs"][1]["header_long_description"] = random_string[7:]
    menu = Menu(c)
    if menu.current_tab_number != 0:
        raise AssertionError
    menu._change_tab(1)
    out, _ = capsys.readouterr()
    if menu.current_tab_number != 1:
        raise AssertionError
    for astr in [
        "Change tab to {}".format(random_string[:3]),
        ": {}".format(random_string[3:7]),
        "\n{}".format(random_string[7:]),
    ]:
        assert out.find(astr) != -1


@pytest.mark.breaking
@pytest.mark.run(order=7)
def test_breaking_change_tab(config_single_with_key, config_single_without_key):
    """Should not work because you can't change tabs with single tabs"""
    for conf in (config_single_with_key, config_single_without_key):
        c = deepcopy(conf)
        menu = Menu(c)
        with pytest.raises(IndexError):
            menu._change_tab(1)


@pytest.mark.regression
@pytest.mark.run(order=8)
def test_method_print_menu(config_all, capsys, data_regression):
    """Simple regression test of print output"""
    menu = Menu(config_all)
    menu._print_menu()
    out, _ = capsys.readouterr()
    data = {"output": out}
    data_regression.check(data)


@pytest.mark.regression
@pytest.mark.run(order=8)
def test_method_print_menu_after_change_tab(config_multiple, capsys, data_regression):
    """Simple regression test of print output"""
    menu = Menu(config_multiple)
    menu._print_menu()
    out_before_change, _ = capsys.readouterr()
    menu._change_tab(1)
    menu._print_menu()
    out, _ = capsys.readouterr()
    # test that different tabs give different outputs
    if out_before_change == out:
        raise AssertionError
    data = {"output": out}
    data_regression.check(data)


@pytest.mark.regression
@pytest.mark.run(order=8)
class TestCollectInput:
    """will monkeypatch the module.input function"""

    def test_method_collect_input_with_valid_input(self, config_all_with_id, data_regression):
        conf, id_ = config_all_with_id
        c = deepcopy(conf)
        c["case_sensitive"] = False  # to get 100% coverage
        menu = Menu(c)
        normal = menu.config
        test_input_valid_entry = normal["tabs"][0]["items"][0]["valid_entries"][0]
        data = {}
        tabbedshellmenus.menu.input = lambda x: test_input_valid_entry
        result = menu._collect_input()
        data["result"] = result
        if id_.find("multiple") != -1:
            test_input_tab = normal["tabs"][1]["header_entry"]
            tabbedshellmenus.menu.input = lambda x: test_input_tab
            result2 = menu._collect_input()
            data["result_multiple"] = result2
        data_regression.check(data)

    def teardown_method(self):
        """Reverts input"""
        tabbedshellmenus.menu.input = input


@pytest.mark.breaking
@pytest.mark.run(order=9)
class TestBreakingCollectInput:
    """Monkeypatches module.input function"""

    def test_break_collect_input(self, config_all, random_string):
        """Tries an invalid input with testing=True so it doesn't go into an infinite loop"""
        c = deepcopy(config_all)
        menu = Menu(c)
        # this assumes that random_string is not a valid entry in the config file
        # this is a pretty darn safe assumption
        tabbedshellmenus.menu.input = lambda x: random_string
        result = menu._collect_input(testing=True)
        if result != "Invalid, try again":
            raise AssertionError

    def teardown_method(self):
        """Reverts input"""
        tabbedshellmenus.menu.input = input


@pytest.mark.integration
@pytest.mark.regression
@pytest.mark.run(order=10)
class TestRun:
    """Monkeypatches module.input function"""

    def test_with_invalid_input(self, config_all, random_string):
        c = deepcopy(config_all)
        menu = Menu(c)
        tabbedshellmenus.menu.input = lambda x: random_string
        result = menu.run(testing_invalid=True)
        if result != "Invalid, try again":
            raise AssertionError

    def test_with_change_tab(self, config_multiple):
        c = deepcopy(config_multiple)
        menu = Menu(c)
        normal = menu.config
        test_input = normal["tabs"][1]["header_entry"]
        tabbedshellmenus.menu.input = lambda x: test_input
        result = menu.run(testing_tab_change=True)
        assert result == {"new_number": 1, "type": "change_tab"}

    def test_with_valid_entry(self, config_all, data_regression):
        c = deepcopy(config_all)
        menu = Menu(c)
        normal = menu.config
        test_input = normal["tabs"][0]["items"][0]["valid_entries"][0]
        tabbedshellmenus.menu.input = lambda x: test_input
        data = {}
        result = menu.run()
        data["result"] = result
        data_regression.check(data)

    def teardown_method(self):
        """Reverts input"""
        tabbedshellmenus.menu.input = input
