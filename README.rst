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

.. image:: https://camo.githubusercontent.com/28a51fe3a2c05048d8ca8ecd039d6b1619037326/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f64652532307374796c652d626c61636b2d3030303030302e737667
    :target: https://github.com/ambv/black

.. image:: https://img.shields.io/badge/python-3.5%7C3.6%7C3.7-blue.svg
    :target: https://www.python.org/

.. image:: https://img.shields.io/badge/platform-linux--64%7Cwin--32%7Cwin--64-lightgrey.svg
    :target: https://github.com/Prooffreader/tabbedshellmenus

.. image:: https://img.shields.io/badge/pypi%20package-tbd-brightgreen.svg
    :target: https://github.com/Prooffreader/tabbedshellmenus

.. image:: https://img.shields.io/badge/implementation-cpython-blue.svg
    :target: https://github.com/Prooffreader/tabbedshellmenus

A *flexible*, **tabbed** menu system to run in the shell and control program
flow interactively

Installation
------------

eventually, ``pip install tabbedshellmenus``

Usage
-----


::

    from tabbedshellmenus import Menu
    myconfig = Menu.safe_read_yaml('path/to/yaml')  # or Menu.read_json() or just pass a dict in the next step
    mymenu = Menu(myconfig)
    result = mymenu.run()

    if result == 'result1':``
        do_this_interesting_thing()``
    elif result == 'result2':``
        do_this_other_thing()``
    # etc...


FAQ:
^^^^

Why can't I return handlers?
    Out of scope for this project at this time, but it's on the
    Wish List. For now, the Menu instance just returns strings 
    which the outer closure can then use to control program flow,
    including defining handlers using control flow/if statement
    based on the string returned by Menu.run().

Why are my return values coming in/out strings?
    To keep things simple, all input and output (return) values are
    converted to string. So if you have
    ``config['tabs'][0]['items][0]['item_inputs'] = [1]``,
    the return value will be '1'.

Why do ``items`` have both 'item_choice_displayed' and 'item_inputs' keys?
    To keep things flexible, you don't have to display exactly
    what you'll accept as input. For example, you could display
    'yes/no' as the suggested answers to a yes or no question, but a
    ctually accept ['y', 'n', 'yes', 'no'], etc.

I have 'case_sensitive' == False, but my return value is still uppercase.
    'case_sensitive' only affects inputs, not outputs


Dependencies:
^^^^^^^^^^^^^

* pyyaml
* schema


TODO:
^^^^^
* Sphinx docs

Wish List:
^^^^^^^^^^

* a way to dynamically silence ("grey out", if this were a GUI menu system)
  certain menu items, which may be desired during program flow, probably by
  passing a list of silenced tab names and return values
* have an option to accept single keypresses instead of multiple keys and
  ENTER with the input() function, using ``msvcrt`` package in Windows
  or ``tty`` and ``termios`` in Mac/Linux. (This will make coverage platform-
  dependent, so it will have to be cumulative on travis and appveyor)