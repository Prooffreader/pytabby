#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Just puts menu.Menu into the top pytabby package namespace"""

# pylama:ignore=W0611,E800  # because used for namespace

from . import _version

from . import menu
from .menu import Menu

__version__ = _version.__version__
