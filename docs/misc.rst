.. _known-issues:

Known Issues
============

:program:`dispatcher` exit code 1
---------------------------------

This issue occurs when the Sploitego scripts are not in the system path of the JVM. To fix this issue you will need to
create symlinks to the Sploitego scripts in one of the directories in your path. Unfortunately, it is not as simple as
adding the directory to your ``$PATH`` variable. For some reason JVM determines its PATH in a different way than
``bash``, ``csh``, etc. The :program:`fixpath.py` script in the ``java`` directory was developed to assist in
determining what directories in the JVM's executable path exist. To run it, just do::

    $ cd java
    $ python fixpath.py
    Checking PATH of JVM and Sploitego...
    Warning /usr/local/bin not in your JVM's PATH
    [0] : /usr/bin
    [1] : /bin
    [2] : /usr/sbin
    [3] : /sbin
    [4] : /opt/local/bin
    ...
    Please select the path where you'd like to place symlinks to Sploitego's scripts [0] : 4
    symlinking /usr/local/bin/dispatcher to /opt/local/bin/dispatcher...
    symlinking /usr/local/bin/sploitego to /opt/local/bin/sploitego...


As seen above, :program:`fixpath.py` compiles ``JVMPathChecker.java`` and runs it to determine the value of the JVM's
PATH environment variable. From that, it provides you with a list of directory options for which to install the
sploitego scripts to. Once you have selected the appropriate directory, :program:`fixpath.py` will then symlink each of
the scripts for you in the directory of your choice.