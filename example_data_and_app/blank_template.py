# I personally don't like using .py files as config files, but I'm no purist, so here's an example.
# note that this is not black-formated, but more compact in space

config = {'case_sensitive': False,
          'screen_width': 80,
          'tabs': [{'header_entry': '',
                    'header_description': '',
                    'header_long_description': '',
                    'items': [{'choice_displayed': '',
                               'choice_description': '',
                               'valid_entries': [''],
                               'returns': '' }
                    ]}]
         }

# # above, but with every line commented with explanation
#
# config = {'case_sensitive': False,  # optional, boolean, default False
#           'screen_width': 80,  # optional, integer, default 80
#           'tabs': [  # optional if only one tab; 'items' key can be at this level in that case
#                    {'header_entry': '',  # required if multiple tabs, forbidden if only one tab, will be changed to str if not already str
#                     'header_description': '',  # optional if multiple tabs, forbidden if only one tab, default None
#                     'header_long_description': '',  # optional if multiple tabs, forbidden if only one tab, default None
#                     'items': [  # if only one tab, this can replace 'tabs' key
#                               {'choice_displayed': '',  # required
#                                'choice_description': '',  # required
#                                'valid_entries': [''],  # list, can have multiple entries, each will be changed to str if not already str
#                                'returns': '' }  # required, will be changed to str if not already str
#                     ]}]
#          }