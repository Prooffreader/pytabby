tabbedshellmenus [in development]
=================================

.. image:: https://secure.travis-ci.org/Prooffreader/tabbedshellmenus.png
    :target: http://travis-ci.org/Prooffreader/tabbedshellmenus

.. image:: https://ci.appveyor.com/api/projects/status/preqq0h4peiad07a?svg=true
    :target: https://ci.appveyor.com/project/Prooffreader/tabbedshellmenus

.. image:: https://api.codacy.com/project/badge/Coverage/dae598fbe5b04b0e90e9e2080bb68c11
    :target: https://www.codacy.com/app/Prooffreader/tabbedshellmenus?utm_source=github.com&utm_medium=referral&utm_content=Prooffreader/tabbedshellmenus&utm_campaign=Badge_Coverage)

.. image:: https://api.codacy.com/project/badge/Grade/dae598fbe5b04b0e90e9e2080bb68c11
    :target: https://www.codacy.com/app/Prooffreader/tabbedshellmenus?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Prooffreader/tabbedshellmenus&amp;utm_campaign=Badge_Grade)

.. image:: https://img.shields.io/badge/python-2.7%7C3.5%7C3.6%7C3.7-blue.svg
    :target: https://github.com/Prooffreader/tabbedshellmenus

.. image:: https://img.shields.io/badge/platform-linux--64%7Cwin--32%7Cwin--64-lightgrey.svg
    :target: https://github.com/Prooffreader/tabbedshellmenus

.. image:: https://img.shields.io/badge/pypi%20package-tbd-brightgreen.svg
    :target: https://github.com/Prooffreader/tabbedshellmenus

.. image:: https://img.shields.io/badge/implementation-cpython-blue.svg
    :target: https://github.com/Prooffreader/tabbedshellmenus

A flexible **tabbed** menu system to run in the shell and control program flow interactively

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

 - a way to dynamically silence ("grey out", if this were a GUI menu system) certain menu items, which may be 
   desired during program flow, probably by passing a list of silenced tab names and return values
