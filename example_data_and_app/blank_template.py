# I personally don't like using .py files as config files, but I'm no purist, so here's an example.
# note that this is not black-formated, but more compact in space

config = {'case_sensitive': False,
          'screen_width': 80,
          'tabs': [{'tab_header_input': '',
                    'tab_header_description': '',
                    'tab_header_long_description': '',
                    'items': [{'item_choice_displayed': '',
                               'item_description': '',
                               'item_inputs': [''],
                               "item_returns": '' }
                    ]}]
         }

# # above, but with every line commented with explanation
#
# config = {'case_sensitive': False,  # optional, boolean, default False
#           'screen_width': 80,  # optional, integer, default 80
#           'tabs': [  # optional if only one tab; 'items' key can be at this level in that case
#                    {'tab_header_input': '',  # required if multiple tabs, forbidden if only one tab, will be changed to str if not already str
#                     'tab_header_description': '',  # optional if multiple tabs, forbidden if only one tab, default None
#                     'tab_header_long_description': '',  # optional if multiple tabs, forbidden if only one tab, default None
#                     'items': [  # if only one tab, this can replace 'tabs' key
#                               {'item_choice_displayed': '',  # required
#                                'item_description': '',  # required
#                                'item_inputs': [''],  # list, can have multiple entries, each will be changed to str if not already str
#                                "item_returns": '' }  # required, will be changed to str if not already str
#                     ]}]
#          }