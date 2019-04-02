"""A simple app that goes through the two example yaml config files, first the multiple tab, then the no-tab.
The only action taken is the choices are printed to stdout, unless the 'quit' item is selected, in which case
either the next config file starts or the program exits after both config files have been run"""

import os

from tabbedshellmenus.menu import Menu

import glob

THIS_FOLDER = os.path.split(__file__)[0]

# in same directory as this app.py script
CONFIG_FILE_NAMES = [os.path.split(x)[-1] for x in glob.glob(os.path.join(THIS_FOLDER, "*.yaml"))]
CONFIG_FILE_NAMES = [x for x in CONFIG_FILE_NAMES if not x.startswith("blank")]


def main(config_filename):
    # use staticmethod to read yaml
    config = Menu.safe_read_yaml(os.path.join(THIS_FOLDER, config_filename))

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


print(__name__)

if __name__ == "__main__":
    for fn in CONFIG_FILE_NAMES:
        print("\n##########")
        print(f"# Using config file {fn}")
        print("##########\n")
        main(fn)
