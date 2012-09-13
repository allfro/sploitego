#################################
:py:mod:`sploitego.metasploit`
#################################

The :py:mod:`sploitego.metasploit` package provides a whole bunch of modules to interact with the Metasploit RPC daemon.
The following sections provide an overview of each of these modules.

:py:mod:`sploitego.metasploit.msfrpc`
=====================================

:py:class:`MsfRpcClient`
------------------------

.. py:class:: MsfRpcClient(password[, username='msf'[, uri='/api/'[, port=55553[, server='localhost'[, ssl=True]]]]])

    :class:`MsfRpcClient` connects and authenticates to an Metasploit RPC daemon. If ``password`` is the only parameter
    specified upon initialization, :class:`MsfRpcClient` will attempt to connect to the Metasploit RPC daemon at
    ``'localhost'`` port ``55553`` with a username of ``'msf'``. The following example illustrates how one would use the
    :class:`MsfRpcClient` to connect to an Metasploit RPC daemon residing on the local machine. First ensure that
    :program:`msfrpcd` is running, like so::

        $ cd /opt/metasploit/msf3
        $ ./msfrpcd -P test
        [*] MSGRPC starting on 0.0.0.0:55553 (SSL):Msg...
        [*] MSGRPC backgrounding at 2012-08-30 22:34:54 -0400...

    Once :program:`msfrpcd` is running, open a python console and try the following::

        >>> from sploitego.metasploit.msfrpc import MsfRpcClient
        >>> m = MsfRpcClient('test')
        >>> print m.modules.exploits
        ('windows/wins/ms04_045_wins', 'windows/vpn/safenet_ike_11', 'windows/vnc/winvnc_http_get', 'windows/vnc/ult ...

    If successful, you should see the full list of exploit modules available for use in your Metasploit distribution.

.. py:method:: MsfRpcClient.call(method, *args)

    Builds and transmits an RPC request and retrieves the result from the Metasploit RPC daemon. This method gets called
    indirectly when using any of the methods provided by the various classes in :py:mod:`sploitego.metasploit.msfrpcd`.
    However, in the odd case where :py:mod:`sploitego.metasploit.msfrpc` and its classes do not provide the
    functionality desired, this method may be used directly to call the desired RPC method in :program:`msfrpcd`. The
    ``method`` argument is a string that identifies the RPC method to call. ``*args`` should contain the RPC arguments
    for the desired RPC method.

.. py:method:: MsfRpcClient.login()

    Authenticates and reauthenticates the :py:class:`MsfRpcClient` object to the :program:`msfrpcd` daemon.

.. py:method:: MsfRpcClient.logout()

    Logs the :py:class:`MsfRpcClient` object out of the :program:`msfrpcd` daemon.

    .. note:: Do not call this method directly.

.. py:attribute:: MsfRpcClient.core

    Returns a :py:class:`CoreManager` object that can be used to manage the Metasploit core.

.. py:attribute:: MsfRpcClient.modules

    Returns a :py:class:`ModuleManager` object that can be used to work with Metasploit exploit, payload, encoder, and
    auxiliary modules.

.. py:attribute:: MsfRpcClient.sessions

    Returns a :py:class:`SessionManager` object that can be used to manage and interact with meterpreter and shell
    sessions.

.. py:attribute:: MsfRpcClient.jobs

    Returns a :py:class:`JobManager` object that can be used to manage Metasploit jobs.

.. py:attribute:: MsfRpcClient.consoles

    Returns a :py:class:`ConsoleManager` object that can be used to manage Metasploit consoles.

.. py:attribute:: MsfRpcClient.plugins

    Returns a :py:class:`PluginManager` object that can be used to manage plugins within Metasploit.

.. py:attribute:: MsfRpcClient.db

    Returns a :py:class:`DbManager` object that can be used to manage Metasploit database connectivity and data as well
    as manage Metasploit workspaces.

.. py:attribute:: MsfRpcClient.auth

    Returns a :py:class:`AuthManager` object that can be used to manage :program:`msfrpcd` sessions and authentication
    tokens.

.. py:attribute:: MsfRpcClient.authenticated

    Returns ``True`` if the :py:class:`MsfRpcClient` object is currently authenticated.

:py:class:`WorkspaceManager`
----------------------------

.. py:class:: DbManager(rpc)

    The :py:class:`DbManager` class can be used to manage a variety of Metasploit database activities such as database
    connectivity, data and workspace management, etc. The ``rpc`` argument is an authenticated :py:class:`MsfRpcClient`
    object. The following example illustrates how to use the :py:class:`DbManager` class::

        >>> from sploitego.metasploit.msfrpc import MsfRpcClient
        >>> m = MsfRpcClient('test')
        >>> dbm = m.db
        >>> print m.db.workspace
        default
        >>>


    .. note:: :py:class:`DbManager` objects are constructed by accessing the :py:attr:`MsfRpcClient.db`
              attribute.

.. py:method:: DbManager.connect(username[, database='msf'[, host='localhost'[, driver='postgresql'[, **kwargs]]]])

    Instructs Metasploit to connect to the ``database`` located at ``host`` using ``driver`` with credentials
    ``username`` and optionally ``password``. Check your Metasploit distribution for a list of supported database driver
    names. As of this writing Metasploit supports the ``'sqlite3'``, ``'mysql'``, ``'postgresql'`` drivers. By default,
    Metasploit uses the ``'postgresql'`` driver. The following example illustrates how to connect to a PostgreSQL
    database on the local machine with a database name of ``'localhost'``::

        >>> m.db.connect(None, database='localhost')
        >>> print m.db.status
        {'db': 'localhost', 'driver': 'postgresql'}


.. py:method:: DbManager.disconnect()

    Instructs Metasploit to disconnect from the database it is currently connected to.

.. py:attribute:: DbManager.driver

    Gets and sets the driver that is being used by Metasploit to establish backend database connectivity.

.. py:attribute:: DbManager.status

    Gets Metasploit's database connectivity status.

.. py:attribute:: DbManager.workspace

    Gets and sets the name of the current workspace being used by Metasploit to store information.

.. py:attribute:: DbManager.workspaces

    Returns a :py:class:`WorkspaceManager` object that can be used to manage and interact with Metasploit workspaces.

:py:class:`WorkspaceManager`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:class:: WorkspaceManager(rpc)

    The :py:class:`WorkspaceManager` object provides an interface for managing and working with Metasploit workspaces.
    It is usually constructed by referencing the :py:attr:`DbManager.workspaces` attribute. The following example
    illustrates how to get an instance of the :py:class:`WorkspaceManager`::

        >>> wm = m.db.workspaces
        >>> print wm.list
        ({'created_at': 1346562727, 'name': 'default', 'updated_at': 1346562727})

    .. note:: :py:class:`WorkspaceManager` objects are constructed by accessing the :py:attr:`DbManager.workspaces`
              attribute.

.. py:method:: WorkspaceManager.workspace([name='default'])

    Returns a :py:class:`Workspace` object that can be used to interact with a Metasploit workspace identified by
    ``name``. If the workspace name does not exist, :py:meth:`WorkspaceManager.workspace` will create it. If no name is
    specified, the ``'default'`` workspace will be returned.

.. py:method:: WorkspaceManager.add(name)

    Creates a Metasploit workspace with the specified ``name``.

.. py:method:: WorkspaceManager.remove(name)

    Destroys and removes the Metasploit workspace identified by ``name``.

.. py:method:: WorkspaceManager.get(name)

    Returns meta-data about the Metasploit workspace identified by ``name`` such as its creation and last updated date-
    timestamps.

.. py:method:: WorkspaceManager.set(name)

    Sets the default Metasploit workspace identified by ``name`` for the current session.

.. py:attribute:: WorkspaceManager.list

    Returns a list of all the Metasploit workspaces stored in the database.

.. py:attribute:: Workspace.current

    Returns the :py:class:`Workspace` object belonging to the default Metasploit workspace.

.. py:class:: Workspace(rpc, name)

    The :py:class:`Workspace` object provides an interface to directly interact with Metasploit workspaces and tables.
    Clients can import information into any of the Metasploit tables via the following methods and attributes:

    * :py:meth:`Workspace.importdata`: upload and import data into the Metasploit database.
    * :py:meth:`Workspace.importfile`: upload and import report files into the Metasploit database.
    * :py:attr:`Workspace.notes`: create, read, update, delete notes in Metasploit database.
    * :py:attr:`Workspace.hosts`: create, read, update, delete discovered hosts in Metasploit database.
    * :py:attr:`Workspace.services`: create, read, update, delete discovered services in Metasploit database.
    * :py:attr:`Workspace.vulns`: create, read, update, delete discovered vulnerabilities in Metasploit database.
    * :py:attr:`Workspace.events`: create, read, update, delete events in Metasploit database.
    * :py:attr:`Workspace.loots`: create, read, update, delete discovered sensitive information in Metasploit database.
    * :py:attr:`Workspace.creds`: create, read, update, delete discovered credentials in Metasploit database.
    * :py:attr:`Workspace.clients`: create, read, update, delete discovered clients in Metasploit database.

    The following example illustrates how to retrieve a :py:class:`Workspace` object::

        >>> w = m.db.workspace.workspace('test')
        >>> print w.current
        test

    .. note:: :py:class:`Workspace` objects are constructed by accessing the :py:meth:`WorkspaceManager.workspace`
              method.

.. py:method:: Workspace.delete()

    Removes and destroys the current workspace in the Metasploit database.

.. py:method:: Workspace.importdata(data)

    Imports arbitrary data into the Metasploit database where ``data`` should be of type :py:class:`str`.

.. py:method:: Workspace.importfile(fname)

    Imports a report file (Nmap, Nessus, etc.) into the Metasploit database identified by the absolute path to the file
    specified in the ``fname`` argument. The file should exist on the filesystem where :program:`msfrpcd` is running.

.. py:attribute:: Workspace.current

    Gets and sets the name of the current Metasploit workspace that is being interacted with.

.. py:attribute:: Workspace.notes

    Returns a :py:class:`NotesTable` object that provides an interface to perform CRUD (create, read, update, delete)
    operations on the Metasploit ``notes`` table. The notes table is used to annotate findings such as vulnerabilities,
    services, hosts, etc.

.. py:attribute:: Workspace.hosts

.. py:attribute:: Workspace.services

.. py:attribute:: Workspace.vulns

.. py:attribute:: Workspace.events

.. py:attribute:: Workspace.loots

.. py:attribute:: Workspace.creds

.. py:attribute:: Workspace.clients




