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

.. image:: https://img.shields.io/badge/code%20style-black-lightgrey.svg
    :target: https://github.com/ambv/black

.. image:: https://img.shields.io/badge/python-2.7%7C3.5%7C3.6%7C3.7-blue.svg
    :target: https://www.python.org/

.. image:: https://img.shields.io/badge/platform-linux--64%7Cwin--32%7Cwin--64-lightgrey.svg
    :target: https://github.com/Prooffreader/tabbedshellmenus

.. image:: https://img.shields.io/badge/pypi%20package-tbd-brightgreen.svg
    :target: https://github.com/Prooffreader/tabbedshellmenus

.. image:: https://img.shields.io/badge/implementation-cpython-blue.svg
    :target: https://github.com/Prooffreader/tabbedshellmenus

A *flexible*, **tabbed** menu system to run in the shell and control program flow interactively

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

NOTE:
^^^^^


FAQ:
^^^^

Why can't I return handlers?
    Out of scope for this project. The Menu instance just returns strings to control program flow, you can put the handlers in if statements after a value is returned.

Why are my values coming in/out strings?
    To keep things simple, all input and output (return) values are converted to string. So if you have config['tabs'][0]['items][0]['valid_entries'] = [1], the return value will be '1'.

Why do ``items`` have both 'choice_displayed' and 'valid_entries' keys?
    To keep things flexible, you don't have to display exactly what you'll accept as input. For example, you could display 'y/n' as the suggested answers to a yes or no question, but actually accept ['y', 'n', 'yes', 'no'], etc.

I have 'case_sensitive' == False, but my return value is still uppercase.
    'case_sensitive' only affects inputs, not outputs

Dependencies:
^^^^^^^^^^^^^

* pyyaml
* schema


TODO:
^^^^^

* test None as header_description and long_description, ensure test cases have descriptions present, absent and None
* test normalizer proper handling of lower case where appropriate
* add another test config with other case
* test that case_sensitive doesn't affect output/return, just header_choice_displayed_and_accepted and valid_entries.
* ^ change example yamls to make this clear
* test whether 'header_description' appears in error messages of test_validators:test_no_multiple_tabs_in_single_with_key
* test whether error messages are being truncated in all vv. of Python
* check this line in test_tab: keys = sorted(tab_dict["input2result"].keys(), key=str) shouldn't they already be str if they've been normalized?
Wish List:
^^^^^^^^^^

* a way to dynamically silence ("grey out", if this were a GUI menu system) certain menu items, which may be desired during program flow, probably by passing a list of silenced tab names and return values
