"""A simple app that shows some capabilities of tabbedshellmenus."""

import glob
import os
import shutil

from tabbedshellmenus import Menu

# to make this a self-contained app, hardcode the config dict

CONFIG = {
    "case_sensitive": False,
    "screen_width": 80,
    "tabs": [{"tab_header_input": "subdirs",
              "items": [{"item_choice_displayed": "c",
                         "item_description": "Create missing subdirectories",
                         "item_inputs": ["c"],
                         "item_returns": "create_subdirs"},
                        {"item_choice_displayed": "h",
                         "item_description": "Help",
                         "item_inputs": ["h"],
                         "item_returns": "help"},
                        {"item_choice_displayed": "q",
                         "item_description": "Quit",
                         "item_inputs": ["q"],
                         "item_returns": "quit"}]},
             {"tab_header_input": "files",
              "items": [{"item_choice_displayed": "i",
                         "item_description": "Move to interesting/",
                         "item_inputs": ["i"],
                         "item_returns": "interesting"},
                        {"item_choice_displayed": "b",
                         "item_description": "Move to boring/",
                         "item_inputs": ["b"],
                         "item_returns": "boring"},
                        {"item_choice_displayed": "s",
                         "item_description": "Skip",
                         "item_inputs": ["s"],
                         "item_returns": "skip"}]}]}


def print_help():
    """Prints help string to stdout"""
    help_text = (
        "This app goes through the contents of a directory and allows you to categorize the files, "
        "either moving them to subdirectories called interesting/ and boring/ or skipping them. This "
        "functionality is handled by the second tab\n    The first tab allows you to check if the "
        "subdirectories already exist, allows you to create them if they are missing, shows this help "
        "text and allows you to quit the app\n"
    )
    print(help_text)


def get_directory():
    """Gets the name of a directory to use, or uses the current one"""
    valid = False
    while not valid:
        directory = input("Enter directory (blank for current): ")
        if directory.strip() == "":
            directory = os.getcwd()
        if os.path.isdir(directory):
            valid = True
        else:
            print("That directory does not exist.")
    return directory


def get_files():
    """Returns a list of files in the current working directory"""
    files = []
    for item in glob.glob("./*"):
        # add current .py file in case it's in the directory
        if os.path.isfile(item) and item != os.path.split(__file__)[1]:
            files.append(item)
    return sorted(files)


def create_subdirectories():
    """Creates subdirectories if they do not exist"""
    for subdir in ["interesting", "boring"]:
        if os.path.isdir(subdir):
            print("./{0}/ EXISTS".format(subdir))
        else:
            os.mkdir(subdir)
            print("./{0}/ CREATED".format(subdir))
    print("")


def move_to_subdir(filename, subdirname):
    """Moves filename to subdirname"""
    if os.path.isfile(os.path.join(subdirname, filename)):
        raise ValueError("File already exists in that subdirectory!")
    shutil.move(filename, subdirname)
    print("{0} moved to ./{1}/".format(filename, subdirname))
    print("")


def main_loop():  # noqa: C901
    """All the logic for the app"""
    menu = Menu(CONFIG)
    files = get_files()
    for i, filename in enumerate(files):
        print("File {0} of {1}: {2}".format(i + 1, len(files), filename))
        interrupt_while = False
        exit_files = False
        while not interrupt_while:
            result = menu.run()
            if result == ("subdirs", "create_subdirs"):
                create_subdirectories()
            elif result == ("subdirs", "help"):
                print_help()
            elif result == ("subdirs", "quit"):
                exit_files = True
            elif result[0] == "files" and result[1] in ["interesting", "boring"]:
                if not os.path.isdir(result[1]):
                    raise ValueError("Directory must be created first")
                move_to_subdir(filename, result[1])
                interrupt_while = True
            elif result == ("files", "skip"):
                interrupt_while = True
            else:
                raise ValueError("Unrecognized input")
        if exit_files:
            break
    if exit_files:
        print("Program exited.")
    else:
        print("All files done.")


if __name__ == "__main__":

    cwd = os.getcwd()
    os.chdir(get_directory())
    main_loop()
    os.chdir(cwd)
