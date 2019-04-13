#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Functions that ensure incoming configs have the same general features AFTER validation.

(This ordering is chosen because if the config doesn't pass validation, the user will have to fix it as they
see it, not as it looks after validation)
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from copy import deepcopy


def _add_tabs_key_if_needed(config):
    if "tabs" not in config.keys():
        if "items" not in config.keys():  # sanity check
            raise AssertionError
        config["tabs"] = [{"items": deepcopy(config["items"])}]
        del config["items"]
        return config
    else:
        return config


def _walk_stringize_and_case(config):  # noqa: C901
    """Walks the various contents of config and:

    1. Converts to string if not None where appropriate
    2. If case_sensitive is False, converts to lowercase where appropriate
    """
    new = {}
    c = config

    def strcase(thing, change_case=False, none_allowed=False):
        if none_allowed and thing is None:
            return None
        if change_case and not config["case_sensitive"]:
            return str(thing).lower()
        else:
            return str(thing)

    for k in ["case_sensitive", "screen_width"]:
        new[k] = c[k]
    new["tabs"] = []
    for tab in c["tabs"]:
        new_tab = {}
        for k1, v1 in tab.items():
            if k1 == "header_entry":
                new_tab[k1] = strcase(v1, True)
            elif k1 in ["header_description", "long_description"]:
                new_tab[k1] = strcase(v1, False, True)
            new_tab["items"] = []
            for item in tab["items"]:
                new_item = {}
                for k2, v2 in item.items():
                    if k2 in ["choice_displayed", "choice_description", "returns"]:
                        new_item[k2] = strcase(v2)
                    else:
                        new_entries = []
                        for entry in item["valid_entries"]:
                            new_entries.append(strcase(entry, True))
                        new_item["valid_entries"] = new_entries
                new_tab["items"].append(new_item)
        new["tabs"].append(new_tab)
    return new


def normalize(config):
    """Runs underscored functions in this module on config dict"""
    config = _add_tabs_key_if_needed(config)
    config = _walk_stringize_and_case(config)
    return config
