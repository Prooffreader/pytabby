#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Functions that ensure incoming configs have the same general features AFTER validation.

The validation check comes first so they user can fix problems as they see it, not after it looks after normalization

Normalization consists of, for those parts of the config that require it:
1. Adding default values where the key is missing
2. Converting elements to string where appropriate
3. Converting elements to lower-case where appropriate if config's case_sensitive is False
"""


from copy import deepcopy


def _add_tabs_key_if_needed(config):
    """Adds redundant 'tab' key if config describes a single tab with 'items' as a top-level key.

    Called from normalize()

    Args:
        config (dict): config dict from menu.Menu

    Returns:
        config (dict): modified so that 'items' key is a member of 'tabs': list if appropriate
                       otherwise, unchanged config
    """
    if "tabs" not in config.keys():
        if "items" not in config.keys():  # sanity check
            raise AssertionError("There is something wrong with the test suite if this error is called")
        config["tabs"] = [{"items": deepcopy(config["items"])}]
        del config["items"]
        return config
    else:
        return config


def _walk_stringize_and_case(config):  # noqa: C901
    """Walks the various contents of config and:

    1. Adds default values if missing
    2. Converts to string if not None where appropriate
    3. If case_sensitive is False, converts to lowercase where appropriate

    Called from normalize()

    Args:
        config (dict): config dict from menu.Menu after possibly being modified by _add_key_if_needed()

    Returns:
        config (dict): modified so that 'items' key is a member of 'tabs': list if appropriate
                       otherwise, unchanged config
    """
    new_config = {}
    old_config = config

    if old_config.get("case_sensitive", None):
        new_config["case_sensitive"] = old_config["case_sensitive"]
    else:
        new_config["case_sensitive"] = False

    if old_config.get("screen_width", None):
        new_config["screen_width"] = old_config["screen_width"]
    else:
        new_config["screen_width"] = 80

    def stringify_and_recase(element, change_case=False, none_allowed=False):
        """Changes to string and/or changes case where appropriate.

        Args:
            element (object): Python object (probably a string or an int) that is a value of config
            change_case (bool): whether to change case if and only if nonlocal variable
                                new_config["case_sensitive"] is true
            none_allowed (bool): whether element is allowed to be None, in which case if it is None,
                                 None is returned
        """
        # return None if element is None and that's allowed
        if none_allowed and element is None:
            return None
        # change to lowercase if appropriate for element and for config's case_sensitive boolean key
        if change_case and not new_config["case_sensitive"]:
            return str(element).lower()
        else:
            # return as-is, but as a string
            return str(element)

    # walk tree of config["tabs"], building a new config tree with modified values where appropriate
    new_config["tabs"] = []
    for old_tab in old_config["tabs"]:
        new_tab = {}
        # Note by iterating over the keys and values present in old_tab, there is no assumption made
        # that any key except for 'items' will be present. Congruity of the presence and types of these
        # keys was already done by the validators module
        for tab_key, old_tab_value in old_tab.items():
            if tab_key == "tab_header_input":
                # since this is an input, it should be lowercased if config is not case-sensitive
                new_tab[tab_key] = stringify_and_recase(old_tab_value, change_case=True)
            elif tab_key in ["tab_header_description", "tab_header_long_description"]:
                # these are allowed to be None (or missing, though that's not checked here), and since
                # they are only printed to stdout, they should not change case
                new_tab[tab_key] = stringify_and_recase(old_tab_value, change_case=False, none_allowed=True)
            # items is the only key this function assumes will be there; its presence was already validated
            # by the validators script
            new_tab["items"] = []
            for old_item in old_tab["items"]:
                new_item = {}
                for item_key, old_item_value in old_item.items():
                    if item_key in ["item_choice_displayed", "item_description", "item_returns"]:
                        # these keys are changed to string only
                        # changing the returns value to a string was a design decision which could be
                        # reversed in future, e.g. so a function could be returned
                        new_item[item_key] = stringify_and_recase(old_item_value)
                    else:
                        # the only other possible key, already validated, is 'item_inputs
                        new_entries = []
                        for old_entry in old_item["item_inputs"]:
                            # since this is an input, it should be lowercased if config is not case sensitive
                            new_entries.append(stringify_and_recase(old_entry, True))
                        new_item["item_inputs"] = new_entries
                new_tab["items"].append(new_item)
        new_config["tabs"].append(new_tab)
    return new_config


def normalize(config):
    """Calls semiprivate functions above to normalize config dict

    This allows menu.Menu and tab.Tab to be simplified, as they don't have to account for allowed variations

    Called from menu.Menu only, not by user

    Args:
        config (dict): config data as passed to menu.Menu instantiator
    Returns:
        (dict): normalized/modified config dict
    """
    config = _add_tabs_key_if_needed(config)
    config = _walk_stringize_and_case(config)
    return config
