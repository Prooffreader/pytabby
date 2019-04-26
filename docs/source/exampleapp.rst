Example app
===========

We're going to use ``pytabby`` to control program flow in an app that takes a directory full of files
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

::

    example_app$ ls
    app.py                              cade-roberts-769333-unsplash.jpg  
    prince-akachi-728006-unsplash.jpg    tyler-nix-597157-unsplash.jpg
    brandon-nelson-667507-unsplash.jpg  colton-duke-732468-unsplash.jpg   
    raj-eiamworakul-514562-unsplash.jpg

There are six jpgs we will classify as interesting or boring, plus the app.py script that is smart enough to ignore itself when moving files.
The ``boring`` and ``interesting`` folders are not yet present.

::

    example_app$ python app.py
    Enter directory (blank for current): 
    
    [subdirs|files]
     ======= ------
    [c] Create missing subdirectories
    [h] Help
    [q] Quit
    ?: c
    ./interesting/ CREATED
    ./boring/ CREATED
    
If we try to create the directories again, we'll just be told they already exist

::

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
    ?: h
    This app goes through the contents of a directory and allows you to
    categorize the files, either moving them to subdirectories called 
    interesting/ and boring/ or skipping them. This functionality is 
    handled by the second tab
        The first tab allows you to check if the subdirectories already 
    exist, allows you to create them if they are missing, shows this help 
    text and allows you to quit the app
    
    
    [subdirs|files]
     ======= ------
    [c] Create missing subdirectories
    [h] Help
    [q] Quit
    ?: files
    Change tab to files
    
    [subdirs|files]
     ------- ======
    [i] Move to interesting/
    [b] Move to boring/
    [s] Skip
    Current_file: 1 of 6: brandon-nelson-667507-unsplash.jpg
    ?: i
    ./brandon-nelson-667507-unsplash.jpg moved to ./interesting/
    
    File moved to interesting
    
    [subdirs|files]
     ------- ======
    [i] Move to interesting/
    [b] Move to boring/
    [s] Skip
    Current_file: 2 of 6: cade-roberts-769333-unsplash.jpg
    ?: b
    ./cade-roberts-769333-unsplash.jpg moved to ./boring/
    
    File moved to boring
    
    [subdirs|files]
     ------- ======
    [i] Move to interesting/
    [b] Move to boring/
    [s] Skip
    Current_file: 3 of 6: colton-duke-732468-unsplash.jpg
    ?: s
    
    [subdirs|files]
     ------- ======
    [i] Move to interesting/
    [b] Move to boring/
    [s] Skip
    Current_file: 4 of 6: prince-akachi-728006-unsplash.jpg
    ?: i
    ./prince-akachi-728006-unsplash.jpg moved to ./interesting/
    
    File moved to interesting
    
    [subdirs|files]
     ------- ======
    [i] Move to interesting/
    [b] Move to boring/
    [s] Skip
    Current_file: 5 of 6: raj-eiamworakul-514562-unsplash.jpg
    ?: i
    ./raj-eiamworakul-514562-unsplash.jpg moved to ./interesting/
    
    File moved to interesting
    
    [subdirs|files]
     ------- ======
    [i] Move to interesting/
    [b] Move to boring/
    [s] Skip
    Current_file: 6 of 6: tyler-nix-597157-unsplash.jpg
    ?: i
    ./tyler-nix-597157-unsplash.jpg moved to ./interesting/
    
    File moved to interesting
    All files done.

Now the program exits, and we can verify all the files are where we expect

::

    example_app$ ls
    app.py  boring  colton-duke-732468-unsplash.jpg  interesting
    example_app$ ls boring/
    cade-roberts-769333-unsplash.jpg
    example_app$ ls interesting/
    brandon-nelson-667507-unsplash.jpg  prince-akachi-728006-unsplash.jpg  
    raj-eiamworakul-514562-unsplash.jpg  tyler-nix-597157-unsplash.jpg