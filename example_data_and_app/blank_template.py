# I personally don't like using .py files as config files, but I'm no purist, so here's an example.
# note that this is not black-formated

config = {'case_sensitive': ,
          'screen_width': ,
          'tabs': [{'header_entry': '',
                    'header_description': '',
                    'long_description': '',
                    'items': [{'choice_displayed': '',
                               'choice_description': '',
                               'valid_entries': [''],
                               'returns': '' }
                    ]}]
         }

# # above, but with every line commented with explanation
#
# config = {'case_sensitive': ,  # optional, boolean, default False
#           'screen_width': ,  # optional, integer, default 80
#           'tabs': [{'header_entry': '',  # required, will be changed to str if not already str
#                     'header_description': '',  # optional, default None, will be changed to str if present, not None and not already str
#                     'long_description': '',  # optional, default None, will be changed to str if present, not None and not already str
#                     'items': [{'choice_displayed': '',  # required, will be changed to str if not already str
#                                'choice_description': '',  # required, will be changed to str if not already str
#                                'valid_entries': [''],  # list, can have multiple entries, each will be changed to str if not already str
#                                'returns': '' }  # required, will be changed to str if not already str
#                     ]}]
#          }