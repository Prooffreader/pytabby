#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contains functions used to format shell text output, i.e. multiline strings sent to stdout"""


def format_menu(config, current_tab_number, line_length, message=None):
    """Creates menu to be displayed to user, called from menu.Menu only, not by user

    Args:
        config (dict): the config dict passed to the Menu instantiator, after normalization
        current_tab_number (int): number of currently selected tab (always 0 for single-tabbed menus)
        line_length (int): value from config
        message (str or None): a message to print from Menu.message

    Returns:
        (str) menu to send to stdout
    """
    # get tabs list of dicts; since this is after normalization, this key will have been inserted
    # if it was missing
    tabs = config["tabs"]
    # build up a list of strings, one per line to send to stdout
    menu = [""]
    # only format headers if there are headers, i.e. if there is more than one tab
    if len(tabs) > 1:
        menu += _format_headers(tabs, current_tab_number, line_length)
    # get items from currently selected tab
    current_tab = tabs[current_tab_number]
    items = current_tab["items"]
    # find maximum length of item_choice_displayed in items to make sure they are equally justified
    max_choice_len = 0
    for item in items:
        max_choice_len = max(max_choice_len, len(item["item_choice_displayed"]))
    # build up one line per item, add to menu list
    for item in items:
        choice = item["item_choice_displayed"]
        description = item["item_description"]
        spacer = " " * (max_choice_len - len(choice))
        menu.append("[{0}{1}] {2}".format(choice, spacer, description))
    # add message if applicable
    if message is not None:
        menu.append(message)
    # return one string by concatenating lines of list
    return "\n".join(menu)


def _format_headers(tabs, current_tab_number, line_length):
    """Formats just the tab portion if the config specifies a multi-tab menu

    Called from format_menu()

    Args:
        tabs (list of tab.Tab): list of Tab objects
        current_tab_number (int): number of currently selected tab (always 0 for single-tabbed menus)
        line_length (int): value from config

    Returns:
        (list of str) individual lines to be sent to stdout representing headers, and
                      indicating the currently selected header
    """
    current_line_length = 0
    # the text identifying all tabs
    top_text = []
    # the text indicating which tab is currently selected
    bottom_text = []
    # build the list of strings tab by tab
    for i, tab in enumerate(tabs):
        abbreviation = tab["tab_header_input"]
        description = tab.get("tab_header_description", None)
        if description is None:
            description = ""
        # use = for currently selected tab, - for other tabs
        if i == current_tab_number:
            bottom_char = "="
        else:
            bottom_char = "-"
        # spacer is only required between abbreviation and description if there is a description
        if description:
            spacer = ":"
        else:
            spacer = ""
        # [ to start first tab, | between tabs and ] to end last tab
        if i == 0:
            start = "["
        else:
            start = "|"
        if i == len(tabs) - 1:
            end = "]"
        else:
            end = ""
        new_top_entry = "{0}{1}{2}{3}{4}".format(start, abbreviation, spacer, description, end)
        # add a line return if the curent line with additional text would go over the maximum line length
        if current_line_length + len(new_top_entry) > line_length - 1:
            top_text.append("\n")
            bottom_text.append("\n")
            current_line_length = 0
        top_text.append(new_top_entry)
        # space below brackets or pipes in line above, - or = below text
        bottom_text.append(" " + bottom_char * (len(new_top_entry) - 1))
        current_line_length += len(new_top_entry)
    # take lists with individual line-break members and turn into list with splits at the line breaks
    top_text = "".join(top_text).split("\n")
    bottom_text = "".join(bottom_text).split("\n")
    # add alternating top and bottom lines to multiline string to return
    total_text = []
    for top, bottom in zip(top_text, bottom_text):
        total_text.append(top)
        total_text.append(bottom)
    return total_text
