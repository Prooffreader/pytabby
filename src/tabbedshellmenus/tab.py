#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Helper functions for menu.Menu and Tab class to represent individual tabs in menu.Menu"""

# pylama:ignore=W293,W291,W391,E302,E128 (will be fixed by black)


def create_tab_objects(config_tabs, case_sensitive):
    """Creates Tab objects in list in order of config_tabs.
    
    :param config_tabs: output of make_config_tabs
    :type config_tabs: dict
    :param case_sensitive: passed from menu
    :type case_sensitive: bool
    :returns: list of Tab objects from menu
    :rtype: list of Tab objects

    NOTE: tab_selectors is list (in tab order) of entries that select tabs
    needed because along with items[:]valid_entries, these are valid entries.
    This will be an empty list for a single tab
    """
    tab_selectors = []
    for tab in config_tabs:
        if tab.get("header_choice_displayed_and_accepted", None):
            tab_selectors.append(tab["header_choice_displayed_and_accepted"])
    tabs = []
    for tab in config_tabs:
        tabs.append(Tab(tab, tab_selectors, case_sensitive))
    return tabs


class Tab:
    """Tab class to represent individual tabs in Menu class
    
    :param tab_dict: passed from menu constructor from config
    :type tab_dict: dict
    :param tab_selectors: all inputs that select tabs
    :type tab_selectors: list
    :param case_sensitive: whether to consider case in selections
    :type case_sensitive: bool
    """

    def __init__(self, tab_dict, tab_selectors, case_sensitive):
        self.head_choice = tab_dict.get("header_choice_displayed_and_accepted", None)
        self.head_desc = tab_dict.get("header_description", None)
        self.head_desc_long = tab_dict.get("long_description", None)
        self.selectors = tab_selectors
        self.case_sensitive = case_sensitive
        self._parse_items(tab_dict["items"])

    def _parse_items(self, items):
        self.input2result = {}
        for i, selector in enumerate(self.selectors):
            cased_selector = selector if self.case_sensitive else selector.lower()
            self.input2result[cased_selector] = {"type": "change_tab", "new_number": i}  # TODO: consider namedtuple?
        for item in items:
            for entry in item["valid_entries"]:
                cased_entry = entry if self.case_sensitive else entry.lower()
                self.input2result[cased_entry] = {"type": "return", "return_value": item["returns"]}

    def process_input(self, inputstr):
        """Called from menu from string user input"""
        if inputstr in self.input2result.keys():
            return self.input2result[inputstr]
        else:
            return {"type": "invalid"}
