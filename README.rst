pytabby
================

.. inclusion-marker-top-of-index

.. image:: https://secure.travis-ci.org/Prooffreader/pytabby.png
    :target: http://travis-ci.org/Prooffreader/pytabby

.. image:: https://ci.appveyor.com/api/projects/status/preqq0h4peiad07a?svg=true
    :target: https://ci.appveyor.com/project/Prooffreader/pytabby

.. image:: https://codecov.io/gh/Prooffreader/pytabby/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Prooffreader/pytabby

.. image:: https://api.codacy.com/project/badge/Grade/dae598fbe5b04b0e90e9e2080bb68c11
    :target: https://www.codacy.com/app/Prooffreader/pytabby?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Prooffreader/pytabby&amp;utm_campaign=Badge_Grade)

.. image:: https://camo.githubusercontent.com/14a9abb7e83098f2949f26d2190e04fb1bd52c06/68747470733a2f2f626c61636b2e72656164746865646f63732e696f2f656e2f737461626c652f5f7374617469632f6c6963656e73652e737667
    :target: https://github.com/Prooffreader/pytabby/blob/master/LICENSE

.. image:: https://camo.githubusercontent.com/28a51fe3a2c05048d8ca8ecd039d6b1619037326/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f64652532307374796c652d626c61636b2d3030303030302e737667
    :target: https://github.com/ambv/black

.. image:: https://img.shields.io/badge/python-3.6%7C3.7-blue.svg
    :target: https://www.python.org/

.. image:: https://img.shields.io/badge/platform-linux--64%7Cwin--32%7Cwin--64-lightgrey.svg
    :target: https://github.com/Prooffreader/pytabby

.. image:: https://badge.fury.io/py/pytabby.svg
    :target: https://pypi.org/project/pytabby

A *flexible, non-opinionated*, **tabbed** menu system to run in the shell and control program
flow interactively. It's a class with one sole public method which runs in a ``while``
loop as you switch tabs (if you want tabs, that is; you're free not to have any) or if you 
enter invalid input, and then returns a string based on the value you selected that
you can use to control the outer program flow.

Of course, you can run the class itself in a ``while`` loop in the enclosing program, getting
menu choice after menu choice returned as you navigate a program.


Installation
------------

``pip install pytabby``

It's just that easy.


Usage
-----

.. code-block:: python

    from pytabby import Menu
    myconfig = Menu.safe_read_yaml('path/to/yaml')
    # or Menu.read_json() or just pass a dict in the next step
    mymenu = Menu(myconfig)
    result = mymenu.run()

    if result == 'result1':
        do_this_interesting_thing()
    elif result == 'result2':
        do_this_other_thing()
    # etc...


See it in action!
-----------------

.. image:: https://www.dtdata.io/shared/pytabby.gif

FAQ
---

***Why did you make this?**
    Well, it was one of those typical GitHub/PyPI scenarios, I wanted a specific thing,
    so I made a specific thing and then I took >10X the time making it a project so that
    others can use the thing; maybe some people will find it useful, maybe not.
    I like running programs in the terminal, and this allowed me to put a bunch of
    utilities like duplicate file finders and bulk file renamers all under one
    umbrella. If you prefer GUIs, there are plenty of simple wrappers out there,

**Why can't I return handlers?**
    Out of scope for this project at this time, but it's on the
    Wish List. For now, the Menu instance just returns strings 
    which the outer closure can then use to control program flow,
    including defining handlers using control flow/if statement
    based on the string returned by Menu.run().

**Why are my return values coming in/out strings?**
    To keep things simple, all input and output (return) values are
    converted to string. So if you have
    ``config['tabs'][0]['items][0]['item_returns'] = 1``,
    the return value will be '1'.

**Why do 'items' have both 'item_choice_displayed' and 'item_inputs' keys?**
    To keep things flexible, you don't have to display exactly
    what you'll accept as input. For example, you could display
    'yes/no' as the suggested answers to a yes or no question, but
    actually accept ['y', 'n', 'yes', 'no'], etc.

**I have 'case_sensitive' = False, but my return value is still uppercase.**
    ``case_sensitive`` only affects inputs, not outputs

**What's up with passing a dict with the tab name as a message to Menu.run()?**
    The message might be different depending on the tab, and ``run()`` 
    only exits when it returns a value when given a valid item input.
    It changes tabs in a loop, keeping that implementation detail 
    abstracted away from the user, as is right.


Dependencies
------------

* ``PyYAML>=5.1``
* ``schema>=0.7.0``

.. inclusion-marker-before-wishlist

Wish List:
----------

.. inclusion-marker-start-wishlist

* a way to dynamically silence ("grey out", if this were a GUI menu system)
  certain menu items, which may be desired during program flow, probably by
  passing a list of silenced tab names and return values
* have an option to accept single keypresses instead of multiple keys and
  ENTER with the input() function, using ``msvcrt`` package in Windows
  or ``tty`` and ``termios`` in Mac/Linux. (This will make coverage platform-
  dependent, so it will have to be cumulative on travis and appveyor)