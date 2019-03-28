# I personally don't like using .py files as config files, but I'm no purist, so here's an example.
# note that this is not black-formated

config = {'case_sensitive': ,
          'screen_width': ,
          'tabs': [{'header_choice_displayed_and_accepted': '',
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
#           'tabs': [{'header_choice_displayed_and_accepted': '',  # all choices can be string length 1+ or int
#                     'header_description': '',  # can be None
#                     'long_description': '',  # this key is optional, it is displayed only when changing tebs
#                     'items': [{'choice_displayed': '',  # any string
#                                'choice_description': '',  # any string
#                                'valid_entries': [''],  # strs and/or ints
#                                'returns': '' }  # str or int
#                     ]}]
#          }