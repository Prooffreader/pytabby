Blank config templates
======================

For your convenience, here are blank config templates in .yaml, .json and .py (dict) formats.
Add tabs and items as desired.

Remember, having only one tab is the same as having no tabs
(there's nothing else to switch to), so in that case the 'tabs' key is optional, you can just have
the 'items' key in the top level. And if you do have a 'tabs' key with only one items,
it can't have 'tab_header_*' keys, because they would be meaningless and the program schema validator thinks you
made a mistake by leaving out the other tabs.

.. literalinclude:: ../../example_configs/blank_template.yaml
  :language: yaml

.. literalinclude:: ../../example_configs/blank_template.json
  :language: json

.. literalinclude:: ../../example_configs/blank_template.py
  :language: python

