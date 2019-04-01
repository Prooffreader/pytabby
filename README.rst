tabbedshellmenus [in development]
=================================

.. image:: https://secure.travis-ci.org/Prooffreader/tabbedshellmenus.png
    :target: http://travis-ci.org/Prooffreader/tabbedshellmenus

A non-opinionated, flexible TABBED menu system to run in the shell and control
program flow interactively

NOTE:
- the config files can use integers instead of strings for several fields, but
internally they are always converted to strings and the return value for
Menu.run() is always a string, e.g. '1'.



Dependencies:
- pyyaml
- schema

NOTE:
- dev-requirements.txt manually copied from Pipfile


TODO:
 - see what happens if one tab but headers defined; ignore or invalid schema?
 - add test case multiple tabs but one has no headers
 - add case sensitive/insensitive test cases
 - test None as header_description and long_description
 - check that ints work as choices and return values
 - mark tests as smoke, unit, regression, integration, etc. @pytest.mark.label,
   can have >1. Change order in tox.ini? Don't forget to search for unmarked


 WISH LIST:
 - a way to dynamically silence certain menu items, probably by passing a list
   of return values
