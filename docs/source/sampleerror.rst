Sample InvalidSchemaError output
================================

To give you an idea of the different error messages (all output at once under one umbrella exception),
let's use the following YAML with many problems, indicated by comments:

.. literalinclude:: ../../example_configs/sampleerror.yaml
    :language: yaml

And here's what happens when we try to initialize a Menu instance with that config:

::

    >>> from tabbedshellmenus import Menu
    >>> config = Menu.safe_read_yaml('sampleerror.yaml')
    >>> menu = Menu(config)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<<path redacted>>tabbedshellmenus/menu.py", line 58, in __init__
        validators.validate_all(self._config)
      File "<<path redacted>>tabbedshellmenus/validators.py", line 388, in validate_all
        raise InvalidInputError("\n".join(printed_message))
    tabbedshellmenus.validators.InvalidInputError: 
    Errors:
    1. schema.SchemaError: Key 'case_sensitive' error: 'This should be a boolean' should be instance of 'bool'
    2. tab#0: schema.SchemaMissingKeyError: Missing key: 'tab_header_input'
    3. tab#0,item#0,valid_entry#0: schema.SchemaError: <lambda>(None) should evaluate to True
    4. tab#2,item#1: schema.SchemaMissingKeyError: Missing key: 'item_returns'
    5. In tab#1, there are repeated input values including tab selectors: [(1, 2)].
    6. In tab#2, there are repeated input values including tab selectors: [('a', 2)].
    >>> 

As you can see, instead of having to fix the errors one by one, the error message output six errors to fix at once.

It's a little unpythonic, but foolish consistency is the hobgoblin of bad design, to paraphrase.

Now, it's possible certain kinds of errors can be 'swallowed' by others, so there's no guarantee that you won't have
to do more than one round of fixes in particularly problematic configs, but this should save you much more than
half your time.



