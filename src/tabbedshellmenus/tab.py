#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Helper functions for menu.Menu and Tab class to represent individual tabs in menu.Menu"""

# pylama:ignore=W293,W291,W391,E302,E128 (will be fixed by black)


def make_config_tabs(config):
    """From any of the three valid schema types (multiple, single_with_key, single_without_key), normalizes to
    create the contents of the first-level 'tab' key (or what it would be were it there)
    
    :param config: config dict passed from menu.Menu
    :type config: dict
    :returns: 'items'
    :rtype: list of dicts, corresponding to config['tabs']
    """
    if config.get("items", None):
        config_tabs = [{"items": config["items"]}]
    else:
        config_tabs = config["tabs"]
    config_tabs = convert_int_to_string(config_tabs)
    return config_tabs


def convert_int_to_string(config_tabs):
    """Converts strs to ints for the following config_tabs fields:
    * [:]header_choice_displayed_and_accepted
    * [:]items[:]choice_displayed
    * [:]items[:]valid_entries[:]
    * [:]items[:]returns
    """

    def int_to_str(item):
        if isinstance(item, int):
            return str(item)
        else:
            return item

    for tab_num, tab in enumerate(config_tabs):
        try:
            config_tabs[tab_num]["header_choice_displayed_and_accepted"] = int_to_str(
                tab["header_choice_displayed_and_accepted"]
            )
        except KeyError:  # single tab
            assert len(config_tabs) == 1  # sanity check
            pass
        for item_num, item in enumerate(tab["items"]):
            config_tabs[tab_num]["items"][item_num]["choice_displayed"] = int_to_str(item["choice_displayed"])
            config_tabs[tab_num]["items"][item_num]["returns"] = int_to_str(item["returns"])
            for entry_num, entry in enumerate(item["valid_entries"]):
                config_tabs[tab_num]["items"][item_num]["valid_entries"][entry_num] = int_to_str(entry)
    return config_tabs


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
