#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylama:ignore=W293,W291,W391,E302,E128,E127,E303,E501,W292 (will be fixed by black)

"""Functions that ensure incoming configs have the same general features AFTER validation.
(This ordering is chosen because if the config doesn't pass validation, the user will have to fix it as they
see it, not as it looks after validation)"""

from copy import deepcopy

from .validators import _determine_schema_type


def add_tabs_key_if_needed(config):
    if _determine_schema_type(config) == 'single_without_tab':
        config['tabs'] = deepcopy(config['items'])
        del config['items']
        return config
    else:
        return config


def walk_stringize_and_case(config):
    """Walks the various contents of config and:
    1. If it can be string or int, converts to string
    2. If case_sensitive is False, converts to lowercase
    """
    case_sensitive = config['case_sensitive']
    for i, tab in enumerate(config['tabs']):
        k = "header_choice_displayed_and_accepted"
        if k in tab.keys():  # congruity of this checked in validators
            config['tabs'][i][k] = str(tab[k])
        if not case_sensitive:
            config['tabs'][i][k] = tab[k].lower()
        for j, item in enumerate(config['tabs'][i]['items']):
            for k in ['choice_displayed', 'returns']:
                config['tabs'][i]['items'][k] = str(item[k])
                if not case_sensitive:
                    config['tabs'][i]['items'][k] = item[k].lower()
            k = 'valid_entries'
            for n, member in enumerate(item[k]):
                config['tabs'][i]['items'][k][n] = str(member)
                if not case_sensitive:
                    config['tabs'][i]['items'][k][n] = member.lower()
                

            
        
