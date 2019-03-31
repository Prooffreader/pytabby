"""A simple app that goes through the two example yaml config files, first the multiple tab, then the no-tab.
The only action taken is the choices are printed to stdout, unless the 'quit' item is selected, in which case
either the next config file starts or the program exits after both config files have been run"""

import os
import sys

from pysimpletabshellmenu.menu import Menu

import glob

CONFIG_FILE_NAMES = glob.glob("*.yaml")
# in same directory as this app.py script
CONFIG_FILE_NAMES = [x for x in CONFIG_FILE_NAMES if not x.startswith("blank")]


def main(config_filename):

    this_dir = os.path.split(os.path.realpath(__file__))[0]

    # use staticmethod to read yaml
    config = Menu.safe_read_yaml(os.path.join(this_dir, config_filename))

    # instantiate
    menu = Menu(config)

    # run, echoing back results
    while True:
        tab_number, tab, value = menu.run()
        print("")
        print(f"RETURNED TAB = {tab} (#{tab_number})")
        print(f"RETURNED VALUE = {value}")

        if value == "quit":
            print("\nQuitting!\n")
            return


if __name__ == "__main__":
    for fn in CONFIG_FILE_NAMES:
        print('\n##########')
        print(f'# Using config file {fn}')
        print('##########\n')
        main(fn)
