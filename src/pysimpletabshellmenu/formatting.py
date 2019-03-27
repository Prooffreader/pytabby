#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contains functions used to format shell text output"""

# pylama:ignore=W293,W291,W391,E302,E128 (will be fixed by black)


def format_menu(tabs, current_number, line_length):
    """Creates menu to be displayed to user, called from menu.Menu only
    
    :returns: menu to display to stdout
    :rtype: str
    """
    menu = [""]
    if len(tabs) > 0:
        menu.append(_format_headers(tabs, current_number, line_length))
    tab = tabs[current_number]
    items = tab["items"]
    # find maximum length of choice_displayed in items for spacing
    max_choice_len = 0
    for item in items:
        max_choice_len = max(max_choice_len, len(item["choice_displayed"]))
    for item in items:
        choice = item["choice_displayed"]
        desc = item["choice_description"]
        spacer = " " * (max_choice_len - len(choice))
        menu.append(f"({choice}{spacer}) {desc}")
    return "\n".join(menu)


def _format_headers(tabs, current_number, line_length):
    current_line_length = 0
    text = []
    for i, tab in enumerate(tabs):
        abbrev = tab["header_choice_displayed_and_accepted"]
        desc = tab.get("header_description", None)
        if i == current_number:
            spacer = "#"
        else:
            if desc:
                spacer = " "
            else:
                spacer = ""
        if desc is None:
            desc = ""
        new_entry = f"[{abbrev}{spacer}{desc}]"
        if current_line_length + len(new_entry) > line_length - 1:
            text.append("\n")
            current_line_length = 0
        text.append(new_entry)
        current_line_length += len(new_entry)
    return "".join(text)
