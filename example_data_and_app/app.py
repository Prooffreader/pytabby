"""A simple app to show a multiple tab example, it just echoes back the return values and keeps going forever."""

import os

from pysimpletabshellmenu.menu import Menu

CONFIG_FILE_NAME = 'multiple_tabs_with_headers.yaml'  # in same directory as this script


def main():

    this_dir = os.path.split(os.path.realpath(__file__))[0]

    # use staticmethod to read yaml
    config = Menu.safe_read_yaml(os.path.join(this_dir, CONFIG_FILE_NAME))

    # instantiate
    menu = Menu(config)

    # run, echoing back results
    while True:
        tab, value = menu.run()
        print('')
        print(f'RETURNED TAB = {tab}')
        print(f'RETURNED VALUE = {value}')


if __name__ == "__main__":
    main()
