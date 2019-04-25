#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Just puts menu.Menu into the top tabbedshellmenus package namespace"""

from . import _version

from . import menu
from .menu import Menu

__version__ = _version.__version__
