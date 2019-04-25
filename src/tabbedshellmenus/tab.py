#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Helper functions for menu.Menu and Tab class to represent individual tabs in menu.Menu"""


def create_tab_objects(config):
    """Creates Tab objects in list in order of (normalized) menu._config['tabs']

    NOTE: tab_selectors is a list (in tab order) of 'header_input' values.
    It is needed because they are valid inputs along with the 'item_inputs' values of each tab
    For a single-tabbed (i.e. no-tabbed) layout, tab_selector == []
    """
    tab_selectors = []
    for tab in config["tabs"]:
        if tab.get("tab_header_input", None):
            tab_selectors.append(tab["tab_header_input"])
    tabs = []
    for tab in config["tabs"]:
        tabs.append(Tab(tab, tab_selectors))
    return tabs


class Tab:
    """Tab class to represent individual tabs in Menu instance

    Methods:
        process_input: called from Menu instance, not user
    """

    def __init__(self, tab_dict, tab_selectors):
        """Instantiator for Tab class instances. Called by Menu instance, not by user.

        Args:
            tab_dict (dict): passed from menu instantiator's _config
            tab_selectors (list): all values of 'header_input' in _config
        """
        self.head_choice = tab_dict.get("tab_header_input", None)
        self.head_desc = tab_dict.get("tab_header_description", None)
        self.head_desc_long = tab_dict.get("tab_header_long_description", None)
        self.selectors = tab_selectors
        self._parse_items(tab_dict["items"])

    def _parse_items(self, items):
        """Creates a dict of possible input values to possible return values"""
        self.input2result = {}
        for i, selector in enumerate(self.selectors):
            self.input2result[selector] = {"type": "change_tab", "new_number": i}
        for item in items:
            for entry in item["item_inputs"]:
                self.input2result[entry] = {"type": "return", "return_value": item["item_returns"]}

    def process_input(self, inputstr):
        """Processes input value from menu instance according to this Tab instance

        Args:
            inputstr (str): menu instance's input

        Returns:
            (dict), with "type" in ['change_tab', 'return' or 'invalid']
        """
        if inputstr in self.input2result.keys():
            return self.input2result[inputstr]
        else:
            return {"type": "invalid"}
