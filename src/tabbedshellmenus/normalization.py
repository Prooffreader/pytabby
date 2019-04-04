#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylama:ignore=W293,W291,W391,E302,E128,E127,E303,E501,W292 (will be fixed by black)

"""Functions that ensure incoming configs have the same general features AFTER validation.
(This ordering is chosen because if the config doesn't pass validation, the user will have to fix it as they
see it, not as it looks after validation)"""

from copy import deepcopy


def _add_tabs_key_if_needed(config):
    if 'tabs' not in config.keys():
        assert 'items' in config.keys()  # sanity check
        config['tabs'] = deepcopy(config['items'])
        del config['items']
        return config
    else:
        return config


def _walk_stringize_and_case(config):
    """Walks the various contents of config and:
    1. Converts to string if not None
    2. If case_sensitive is False, converts to lowercase
    """
    case_sensitive = config['case_sensitive']
    for i, tab in enumerate(config['tabs']):
        for k, v in tab.keys():
            if k != 'items' and v is not None:
                config['tab'][i][k] = str(tab[k])
                if not case_sensitive:
                    config['tabs'][i][k] = tab[k].lower()
        for j, item in enumerate(config['tabs'][i]['items']):
            for k, v in item.keys():
                if item != 'valid_entries':
                    config['tabs'][i]['items'][k] = str(item[k])
                    if not case_sensitive:
                        config['tabs'][i]['items'][k] = item[k].lower()
                else:
                    for n, member in enumerate(item[k]):
                        config['tabs'][i]['items'][k][n] = str(member)
                        if not case_sensitive:
                            config['tabs'][i]['items'][k][n] = member.lower()


def normalize(config):
    """Runs underscored functions in this module on config dict"""
    config = _add_tabs_key_if_needed(config)
    config = _walk_stringize_and_case(config)
    return config
                

            
        
