Tutorial
========

Everything depends on a good, valid config file. For this tutorial, we'll use the 
following short YAML (found in the Github repo as ``example_configs/tutorial.yaml)``:

.. literalinclude:: ../../example_configs/tutorial.yaml
  :language: yaml

This is a config for two tabs, each with two choices.

First, import the ``Menu`` class:

>>> from tabbedshellmenus import Menu

Then, you need a config file. There are two static methods you can call from the
uninstantiated class, ``safe_read_yaml(path)`` and ``read_json`` path. Or you can
write a python dict and pass that. Here, let's read the YAML file.

>>> config = Menu.safe_read_yaml('tutorial.yaml')  # the file shown above

And now instantiate the class with the config dict:

>>> menu = Menu(config)

At this point, if your config has an invalid schema, the Menu class will raise an InvalidSchemaError
and will output **ALL** the schema violations to stderr. (As opposed to raising just one, Then
you fixing it, then raising another, you fixing it, etc.) 

If the menu instance is instantiated without errors, you can just run it!

>>> menu.run()

You'll see the following printed to stdout:

::

    [a:Menu a|b]
     ======== --
    [1] First choice
    [2] Second choice
    ?: ▓

Note that the first tab, a, is underlined, showing that it's the active tab. Tab b has no description in the config, so it's very short.

Now enter 'c' (an invalid choice) at the prompt. A new line appears (the program does not resend the entire meny to stdout):

::

    ?: c
    Invalid, try again: ▓

Now enter 'b' to switch to that tab. The following is sent to stdout:

::

    Invalid, try again: b
    Change tab to b
    You have just selected Menu B
    
    [a:Menu a|b]
     -------- ==
    [x,y,x] x or y or z
    [q    ] Quit
    ?: ▓

As you can see, the second tab, ``b``, is now underlined. (It really is more obvious if you use descriptions.)

The program output ``Change tab to\ `` & the tab_header_input

Since for this second tab, 'tab_long_description' was defined, that was printed as well (``You have just selected Menu B``, how boring).

Now let's actually submit a valid choice (an invalid choice will give the same 'Invalid, try again: ' message as above).

:: 

    ?: x

    ('b', 'xyz')

Now the menu has returned a value, a tuple of the tab input and the return value. The tuple is returned because different tabs could
have the same return value. If there were only one tab, only the return value ``'xyz'`` would have been returned.






