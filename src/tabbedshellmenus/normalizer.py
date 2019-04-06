#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylama:ignore=W293,W291,W391,E302,E305,E128,E127,E303,E501,W292 (will be fixed by black)

"""Functions that ensure incoming configs have the same general features AFTER validation.
(This ordering is chosen because if the config doesn't pass validation, the user will have to fix it as they
see it, not as it looks after validation)"""

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

from copy import deepcopy


def _add_tabs_key_if_needed(config):
    if "tabs" not in config.keys():
        assert "items" in config.keys()  # sanity check
        config["tabs"] = deepcopy(config["items"])
        del config["items"]
        return config
    else:
        return config


def _walk_stringize_and_case(config):  # noqa: C901
    """Walks the various contents of config and:
    1. Converts to string if not None
    2. If case_sensitive is False, converts to lowercase
    """
    case_sensitive = config["case_sensitive"]
    for i, tab in enumerate(config["tabs"]):
        for k, v in tab.items():
            if k != "items" and v is not None:
                config["tabs"][i][k] = str(tab[k])
                if not case_sensitive:
                    config["tabs"][i][k] = config["tabs"][i][k].lower()
        for j, item in enumerate(config["tabs"][i]["items"]):
            for k, v in item.items():
                if k != "valid_entries":
                    config["tabs"][i]["items"][j][k] = str(v)
                    if not case_sensitive:
                        config["tabs"][i]["items"][j][k] = config["tabs"][i]["items"][j][k].lower()
                else:
                    for n, member in enumerate(v):
                        config["tabs"][i]["items"][j]["valid_entries"][n] = str(member)
                        if not case_sensitive:
                            config["tabs"][i]["items"][j]["valid_entries"][n] = config["tabs"][i]["items"][j][
                                "valid_entries"
                            ][n].lower()
    return config


def normalize(config):
    """Runs underscored functions in this module on config dict"""
    config = _add_tabs_key_if_needed(config)
    config = _walk_stringize_and_case(config)
    return config
