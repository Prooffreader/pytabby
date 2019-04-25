#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contains Menu class; this is the base imported class of this package"""


import json

import yaml

from . import formatting, normalizer, tab, validators


class Menu:
    """Base class to import to create a menu

    Args:
        config (dict): a nested dict, in a schema which will be validated, containing everything needed
                        to instantiate the Menu class
        start_tab_number(int): default 0, the number of the tab to start at

    Methods:
        safe_read_yaml(path_to_yaml): static method to read a yaml file into a config dict
        read_json(path_to_json): static method to read a json file into a config dict
        run(message=None): Displays menu at currently selected tab, asks for user input and returns it as a string

    Examples:

        >>> config = Menu.safe_read_yaml('config.yaml')
        >>> menu = Menu(config, start_tab_number=0)
        >>> result = menu.run()
        >>> if result = "action name":
        >>>         my_great_function()

        >>> # with a submenu
        >>> config = Menu.safe_read_yaml('config.yaml')
        >>> menu = Menu(config, start_tab_number=0)
        >>> result = menu.run()
        >>> if result = "further options":
        >>>     submenu = Menu(submenu_config)
        >>>     if submenu_result = "action name":
        >>>         my_great_function()
    """

    def __init__(self, config, start_tab_number=0):
        """Instantiator for Menu class.

        Args:
            config (dict): a nested dict, in a schema which will be validated, containing everything needed
                           to instantiate the Menu class
            start_tab_number(int): default 0, the number of the tab to start at
        """
        self._config = config
        self._set_testing()
        # validate config
        validators.validate_all(self._config)
        # normalize config
        self._config = normalizer.normalize(self._config)

        self._current_tab_number = start_tab_number
        self._screen_width = self._config.get("screen_width", 80)
        self._has_multiple_tabs = len(self._config["tabs"]) > 1
        # ensure start_tab_number is valid
        if not self._current_tab_number < len(self._config["tabs"]):
            raise AssertionError
        self._create_tab_objects()
        # this attribute is only used by the instance to change user input where required;
        # the config contents have already been altered by the normalizer module
        self._case_sensitive = config.get("case_sensitive", False)

    @staticmethod
    def safe_read_yaml(path_to_yaml):
        """Reads yaml file at specified path.

        Args:
            path_to_yaml (str or pathlib.Path): path to a yaml file following the config schema

        Returns:
            (dict) config to pass to Menu instantiator
        """
        with open(path_to_yaml, "r") as f:
            dict_ = yaml.safe_load(f.read())
        return dict_

    @staticmethod
    def read_json(path_to_json):
        """Reads json file at specified path.

        Args:
            path_to_json (str or pathlib.Path): path to a json file following the config schema

        Returns:
            (dict) config to pass to Menu instantiator
        """
        with open(path_to_json, "r") as f:
            dict_ = json.load(f)
        return dict_

    def _set_testing(self):
        """Sets self._testing to False during normal operation.

        During testing, this can be monkeypatched to one of the following values:
        1. 'collect_input' when testing that function
        2. 'run_tab' when testing tab changing in run()
        3. 'run_invalid' when testing run() with invalid input
        4. 'message' when testing run() with messages
        """
        self._testing = False

    def _create_tab_objects(self):
        """Calls function in tab module"""
        self._tabs = tab.create_tab_objects(self._config)

    def _change_tab(self, new_number):
        """Changes the active tab. Only called from Menu instance .run()"""
        # print message about new selection
        new_tab = self._tabs[new_number]
        # display a message, including description and long_description if present,
        # informing user about the tab change
        if new_tab.head_choice:  # Should be redundant, because should only be called if
            # the config's layout is multiple tabs.
            msg = ["Change tab to {0}".format(new_tab.head_choice)]
            if new_tab.head_desc:
                msg.append(": {0}".format(new_tab.head_desc))
            if new_tab.head_desc_long:
                msg.append("\n{0}".format(new_tab.head_desc_long))
            print("".join(msg))
        self._current_tab_number = new_number

    def _print_menu(self, message=None):
        """Prints formatted menu to stdout"""
        formatted = formatting.format_menu(self._config, self._current_tab_number, self._screen_width, message)
        print(formatted)

    def _collect_input(self):
        """Gets choice from user, repeating until a valid choice given

        Returns:
            (dict) containing info about input, e.g. whether it's a new tab or something that leads to
                   an input_returns value
        """
        # flag
        received_valid_input = False
        prompt = "?"
        if self._testing == "message":
            return prompt
        while not received_valid_input:
            selection = input("{0}: ".format(prompt))  # the 'input' built-in is monkeypatched for testing
            # change input to lower-case if config is not case sensitive
            if not self._case_sensitive:
                selection = selection.lower()
            # call tab.Tab.process_input() function on current tab
            return_dict = self._tabs[self._current_tab_number].process_input(selection)
            if return_dict["type"] == "invalid":
                prompt = "Invalid, try again"
            else:
                received_valid_input = True
            if self._testing in ["run_invalid", "collect_input"]:  # To avoid infinite loop in test
                return prompt
        return return_dict

    def _validate_message(self, message):
        """If run() is called with message as a dict, validates that all keys are valid tab_header_inputs.

        If message is None or string, does nothing.

        Raises:
            ValueError if keys do not match tab_header_inputs
        """
        if isinstance(message, dict):
            if not self._has_multiple_tabs:
                raise ValueError("Menu instance has only one tab, so cannot take a dict as message arg for run()")
            nonmatching_keys = []
            for key in message.keys():
                if not any([x == key for x in self._tabs[0].selectors]):
                    nonmatching_keys.append(key)
            if nonmatching_keys:
                raise ValueError(
                    "The following key(s) in message dict do not match tab_header_inputs: {}".format(
                        "; ".join(nonmatching_keys)
                    )
                )
        else:
            if not isinstance(message, str) and message is not None:
                raise TypeError("message arg to run() must be None, str or dict")

    def _get_message(self, message):
        """Returns None or str or dict's value, as appropriate"""
        if not isinstance(message, dict):
            return message
        current_selector = self._tabs[0].selectors[self._current_tab_number]
        return message.get(current_selector, None)

    def run(self, message=None):
        """Called by user, runs menu until valid selection from a tab is made, and returns value

        Args:
            message (None, str or dict(str: str)): a message to display when the menu is shown.
                If it is a string, it will be shown at every iteration of the menu being shown
                until a valid item input is received and the function returns a value.
                If it is a dict, it should be key=tab_header_input and value=string message
                to be shown only when the current tab equals the key. There can be multiple
                key/value pairs.

        Returns:
            (str, str) or str: if there are multiple tabs, returns tuple of
                (tab_header_input, input_returns value). If there is only one tab, returns
                input_returns value only.
        """
        self._validate_message(message)
        # flag
        received_return_value = False
        while not received_return_value:
            message_ = self._get_message(message)
            self._print_menu(message_)
            return_dict = self._collect_input()
            if self._testing in ["run_invalid", "message"]:
                return return_dict
            if return_dict["type"] == "change_tab":
                self._change_tab(return_dict["new_number"])
                if self._testing == "run_tab":
                    return return_dict
            else:
                if self._has_multiple_tabs:
                    tab_id = self._tabs[self._current_tab_number].head_choice
                    return (tab_id, return_dict["return_value"])
                else:
                    return return_dict["return_value"]
