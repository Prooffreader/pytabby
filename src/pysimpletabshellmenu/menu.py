#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contains Menu class; this is the base imported class of this package"""

import json
from pathlib import Path

import yaml

from .tab import Tab


class Menu:
    """Base class to import to create a menu

    Contains staticmethods 'safe_read_yaml' and 'read_json' to create
    expected config dict from config files. Dict's schema is validated
    before use. (see examples directory in repo)

    :param config: nested data structure containing all info used to make menu
    :type config: dict
    """

    def __init__(self, config):
        self.config = config

    @staticmethod
    def safe_read_yaml(path_to_yaml):
        """Reads yaml file at specified path.

        :param path_to_yaml: path to config yaml file
        :type path_to_yaml: str or pathlib.Path
        :returns: config to pass instantiate Menu
        :rtype: dict
        """
        with open(path_to_yaml, 'r') as f:
            dict_ = yaml.safe_load(f)
        return dict_

    @staticmethod
    def read_json(path_to_json):
        """Reads json file at specified path.

        :param path_to_json: path to config json file
        :type path_to_yaml: str or pathlib.Path
        :returns: config to pass instantiate Menu
        :rtype: dict
        """
        with open(path_to_json, 'r') as f:
            dict_ = json.load(f)
        return dict_

    def _parse_input(self):
        """Creates Tab objects"""
        pass  # TODO

    def run(self):
        """Shows menu, collects input, changes tab and runs again or returns value"""
        pass  # TODO
