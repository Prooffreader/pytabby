#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contains Menu class; this is the base imported class of this package"""

# pylama:ignore=W293,W291,W391,E302 (will be fixed by black)

import json

import yaml

from . import validators
from . import formatting
from .tab import Tab


class Menu:
    """Base class to import to create a menu

    Contains staticmethods 'safe_read_yaml' and 'read_json' to create expected config dict from config files. Dict's 
    schema is validated before use. (see examples or tests/data directory in repo )

    :param config: nested data structure containing all info used to make menu
    :type config: dict
    :param config: start_tab_number: the (zero-based) position of the starting selected tab; handy when saving
                   state between Menu instantiations. Default 0
    "type config: int
    """

    def __init__(self, config, start_tab_number=0):
        self.config = config
        # validate config
        validators.validate_all(self.config)
        self.current_tab_number = start_tab_number
        self._parse_config()

    @staticmethod
    def safe_read_yaml(path_to_yaml):
        """Reads yaml file at specified path.

        :param path_to_yaml: path to config yaml file
        :type path_to_yaml: str or pathlib.Path
        :returns: config to pass to instantiate Menu
        :rtype: dict
        """
        with open(path_to_yaml, "r") as f:
            dict_ = yaml.safe_load(f)
        return dict_

    @staticmethod
    def read_json(path_to_json):
        """Reads json file at specified path.

        :param path_to_json: path to config json file
        :type path_to_yaml: str or pathlib.Path
        :returns: config to pass to instantiate Menu
        :rtype: dict
        """
        with open(path_to_json, "r") as f:
            dict_ = json.load(f)
        return dict_

    def _parse_config(self):
        """Creates Tab objects"""
        self.case_sensitive = self.config.get("case_sensitive", False)
        self.screen_width = self.config.get("screen_width", 80)
        if self.config.get("items", None):
            self.config_tabs = [{"items": self.config["items"]}]
        else:
            self.config_tabs = self.config["tabs"]
        self.tab_selectors = []
        self._convert_int_to_string()
        for tab in self.config_tabs:
            if tab.get("header_choice_displayed_and_accepted", None):
                self.tab_selectors.append(tab["header_choice_displayed_and_accepted"])
        assert self.current_tab_number < len(self.config_tabs)
        self.tabs = []
        for tab in self.config_tabs:
            self.tabs.append(Tab(tab, self.tab_selectors, self.case_sensitive))

    def _convert_int_to_string(self):
        """Converts strs to ints for the following fields:
        tabs:-:header_choice_displayed_and_accepted
        tabs:-:items:-:choice_displayed
        tabs:-:items:-:valid_entries:-:
        tabs:-:items:-:returns
        """

        def int_to_str(item):
            if isinstance(item, int):
                return str(item)
            else:
                return item

        for tab_num, tab in enumerate(self.config_tabs):
            try:
                self.config_tabs[tab_num]["header_choice_displayed_and_accepted"] = int_to_str(
                    tab["header_choice_displayed_and_accepted"]
                )
            except KeyError:  # single tab
                assert len(self.config_tabs) == 1  # sanity check
                pass
            for item_num, item in enumerate(tab["items"]):
                self.config_tabs[tab_num]["items"][item_num]["choice_displayed"] = int_to_str(
                    item["choice_displayed"]
                )
                self.config_tabs[tab_num]["items"][item_num]["returns"] = int_to_str(item["returns"])
                for entry_num, entry in enumerate(item["valid_entries"]):
                    self.config_tabs[tab_num]["items"][item_num]["valid_entries"][entry_num] = int_to_str(entry)

    def _change_tab(self, new_number):
        """Changes the active tab"""
        # print message about new selection
        new_tab = self.tabs[new_number]
        if new_tab.head_choice:
            msg = [f"Change tab to {new_tab.head_choice}"]
            if new_tab.head_desc:
                msg.append(f": {new_tab.head_desc}")
            if new_tab.head_desc_long:
                msg.append(f"\n{new_tab.head_desc_long}")
            print("".join(msg))
        self.current_tab_number = new_number

    def _print_menu(self):
        formatted = formatting.format_menu(self.config_tabs, self.current_tab_number, self.screen_width)
        print(formatted)

    def _collect_input(self):
        received_valid_input = False
        prompt = "?"
        while not received_valid_input:
            selection = input(f"{prompt}: ")  # monkeypatch for testing
            if not self.case_sensitive:
                selection = selection.lower()
            return_dict = self.tabs[self.current_tab_number].process_input(selection)
            if return_dict["type"] == "invalid":
                prompt = "Invalid, try again"
                continue
            else:
                received_valid_input = True
        return return_dict

    def run(self):
        """Called by user, runs menu until valid selection from a tab is made, and returns value
        
        :returns: tuple of tab_number, tab header choice, return value
        :rtype: (int, str or None, str)

        Note that the first item in the tuple is None if there is only one tab/are no tabs
        """
        received_return_value = False
        while not received_return_value:
            self._print_menu()
            return_dict = self._collect_input()
            if return_dict["type"] == "change_tab":
                self._change_tab(return_dict["new_number"])
                continue
            else:
                received_return_value = True
                if self.tab_selectors:
                    tab_id = self.tab_selectors[self.current_tab_number]
                else:
                    tab_id = None
        return (self.current_tab_number, tab_id, return_dict["return_value"])
