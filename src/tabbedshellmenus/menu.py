#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contains Menu class; this is the base imported class of this package

NOTE: When ruamel.yaml v15 API gets finalized, yaml reader code will have to change"""

# pylama:ignore=W293,W291,W391,E302 (will be fixed by black)

import json

import yaml

from . import validators
from . import formatting
from . import normalizer
from . import tab


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
        # normalize config
        self.config = normalizer.normalize(self.config)
        self.current_tab_number = start_tab_number
        self.screen_width = self.config.get("screen_width", 80)
        self.has_multiple_tabs = len(self.config["tabs"]) > 1
        assert self.current_tab_number < len(self.config["tabs"])
        self._create_tab_objects()
        self.case_sensitive = config.get("case_sensitive", False)  # for user input

    @staticmethod
    def safe_read_yaml(path_to_yaml):
        """Reads yaml file at specified path.

        :param path_to_yaml: path to config yaml file
        :type path_to_yaml: str or pathlib.Path
        :returns: config to pass to instantiate Menu
        :rtype: dict
        """
        with open(path_to_yaml, "r") as f:
            dict_ = yaml.safe_load(f.read())
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

    def _create_tab_objects(self):
        self.tabs = tab.create_tab_objects(self.config)

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
        """Prints formatted menu to stdout"""
        formatted = formatting.format_menu(self.config, self.current_tab_number, self.screen_width)
        print(formatted)

    def _collect_input(self):
        """Gets choice from user, repeating until a valid choice given"""
        received_valid_input = False
        prompt = "?"
        while not received_valid_input:
            selection = input(f"{prompt}: ")  # monkeypatch for testing
            if not self.case_sensitive:
                selection = selection.lower()
            return_dict = self.tabs[self.current_tab_number].process_input(selection)
            if return_dict["type"] == "invalid":
                prompt = "Invalid, try again"
            else:
                received_valid_input = True
        return return_dict

    def run(self):
        """Called by user, runs menu until valid selection from a tab is made, and returns value
        
        :returns: if there is more than one tab, returns tuple of (tab selector, return value). 
                  If there is only one tab, returns return value only.
        :rtype: either (str, str) or str
        """
        received_return_value = False
        while not received_return_value:
            self._print_menu()
            return_dict = self._collect_input()
            if return_dict["type"] == "change_tab":
                self._change_tab(return_dict["new_number"])
            else:
                if self.has_multiple_tabs:
                    tab_id = self.tabs[self.current_tab_number].head_choice
                    return (tab_id, return_dict["return_value"])
                else:
                    return return_dict["return_value"]
