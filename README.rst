tabbedshellmenus [in development]
=================================

.. image:: https://secure.travis-ci.org/Prooffreader/tabbedshellmenus.png
    :target: http://travis-ci.org/Prooffreader/tabbedshellmenus

.. image:: https://ci.appveyor.com/api/projects/status/preqq0h4peiad07a?svg=true
    :target: https://ci.appveyor.com/project/Prooffreader/tabbedshellmenus

.. image:: https://coveralls.io/repos/github/Prooffreader/tabbedshellmenus/badge.svg?branch=master
    :target: https://coveralls.io/github/Prooffreader/tabbedshellmenus?branch=master

.. image:: https://img.shields.io/badge/python-2.7%7C3.5%7C3.6%7C3.7-blue.svg

.. image:: https://img.shields.io/badge/platform-linux--64%7Cwin--32%7Cwin--64-lightgrey.svg

.. image:: https://img.shields.io/badge/pypi%20package-tbd-brightgreen.svg

.. image:: https://img.shields.io/badge/implementation-cpython-blue.svg

A flexible **tabbed* menu system to run in the shell and control
program flow interactively

NOTE:
- the config files can use values other than strings for input and output fields, but
internally they are always converted to strings and the return value for
Menu.run() is always a string, e.g. '1'.



Dependencies:
- pyyaml
- schema


TODO:
 - test None as header_description and long_description


 WISH LIST:
 - a way to dynamically silence certain menu items, probably by passing a list
   of silenced tab names and return values
