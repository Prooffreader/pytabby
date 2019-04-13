"""A simple app that shows capabilities of tabbedshellmenus.

Itgoes through the two example yaml config files, first the multiple tab, then the no-tab.
The only action taken is the choices are printed to stdout, unless the 'quit' item is selected, in which case
either the next config file starts or the program exits after both config files have been run
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import glob
import os

from tabbedshellmenus import Menu

THIS_FOLDER = os.path.split(__file__)[0]

# in same directory as this app.py script
CONFIG_FILE_NAMES = [os.path.split(x)[-1] for x in glob.glob(os.path.join(THIS_FOLDER, "*.yaml"))]
CONFIG_FILE_NAMES = [x for x in CONFIG_FILE_NAMES if not x.startswith("blank")]


def main(config_filename):
    """Main function"""
    # use staticmethod to read yaml
    config = Menu.safe_read_yaml(os.path.join(THIS_FOLDER, config_filename))

    # instantiate
    menu = Menu(config)

    # run, echoing back results
    while True:
        returned = menu.run()
        if isinstance(returned, tuple):  # normally wouldn't have to do this, it's because this script
            # is cycling through different kinds of config files
            tab_return = returned[0]
            # find tab number for output
            for tab_number, tab in enumerate(config["tabs"]):
                if tab["header_entry"] == tab_return:
                    break
            else:
                raise AssertionError("Somehow invalid tab choice was returned")
            value_return = returned[1]
        else:
            tab_number = -1
            tab_return = None
            value_return = returned

        print("")
        if tab_return:
            print("RETURNED TAB = {0} (#{1})".format(tab_return, tab_number))
        print("RETURNED VALUE = {0}".format(value_return))

        if value_return == "quit":
            print("\nQuitting!\n")
            return


if __name__ == "__main__":
    for config_file_num, fn in enumerate(CONFIG_FILE_NAMES):
        msg = "# using config file {}/{}: {}".format(config_file_num + 1, len(CONFIG_FILE_NAMES), fn)
        print("\n" + ("#" * len(msg)))
        print(msg)
        print(("#" * len(msg)) + "\n")
        main(fn)
