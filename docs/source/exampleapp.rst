Example app
===========

We're going to use ``tabbedshellmenus`` to control program flow in an app that takes a directory full of files
and allows you to categorize them into subdirectories.

There are two menus: [d]irectory management, where we see if folders exist and create them if needed;
and [f]ile management, where we assign files to subfolders.

Our subfolders will be named ``interesting`` and ``boring``.

Here's the python file, ``app.py``. (It can also be found in the project github repo under example_app/). Instead
of dealing with an external YAML config file, I've just hardcoded the config as a dict into the python app:

.. literalinclude:: ../../example_app/app.py
  :language: python

You can try this out on any folder of files; in the GitHub repo, there's a folder called example_app with this 
script, ``app.py``, and six photos downloaded from `Unsplash <https://unsplash.com>`_, and resized to take up
less space. Note that this program doesn't *show* the images, but feel free to build that capability into it!

Here's an example terminal session using the above script:

(tabsh) prooff@dts76:~/MyPython/venvs/tabsh/tabbedshellmenus/example_app$ ls
app.py                              cade-roberts-769333-unsplash.jpg  prince-akachi-728006-unsplash.jpg    tyler-nix-597157-unsplash.jpg
brandon-nelson-667507-unsplash.jpg  colton-duke-732468-unsplash.jpg   raj-eiamworakul-514562-unsplash.jpg
(tabsh) prooff@dts76:~/MyPython/venvs/tabsh/tabbedshellmenus/example_app$ echo 'Note that app.py is in the same directory, but the app is smart enough to ignore its own file'
Note that app.py is in the same directory, but the app is smart enough to ignore its own file
(tabsh) prooff@dts76:~/MyPython/venvs/tabsh/tabbedshellmenus/example_app$ echo 'Note also that the subdirectories do not yet exist. The app will create them.'
Note also that the subdirectories do not yet exist. The app will create them.
(tabsh) prooff@dts76:~/MyPython/venvs/tabsh/tabbedshellmenus/example_app$ python app.py
Enter directory (blank for current): 

(tabsh) prooff@dts76:~/MyPython/venvs/tabsh/tabbedshellmenus/example_app$ python app.py
Enter directory (blank for current): 

[subdirs|files]
 ======= ------
[c] Create missing subdirectories
[h] Help
[q] Quit
?: c
./interesting/ CREATED
./boring/ CREATED

[subdirs|files]
 ======= ------
[c] Create missing subdirectories
[h] Help
[q] Quit
?: c
./interesting/ EXISTS
./boring/ EXISTS


[subdirs|files]
 ======= ------
[c] Create missing subdirectories
[h] Help
[q] Quit
?: files
Change tab to files