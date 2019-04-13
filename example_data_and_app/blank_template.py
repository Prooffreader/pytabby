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
#           'tabs': [{'header_entry': '',  # required, the input entry required to select that tab
#                     'header_description': '',  # can be missing or None
#                     'header_long_description': '',  # can be missing or None
#                     'items': [{'choice_displayed': '',  # required, will be changed to str if not already str
#                                'choice_description': '',  # required, will be changed to str if not already str
#                                'valid_entries': [''],  # list, can have multiple entries, each will be changed to str if not already str
#                                'returns': '' }  # required, will be changed to str if not already str
#                     ]}]
#          }