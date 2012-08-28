==================
Framework Overview
==================

Sploitego Local Transform Execution
===================================

Local transforms in Maltego execute on the client's local machine by executing a local script or executable and
listening for results on ``stdout`` (or standard output). Sploitego provides a single script for local transform
execution called :program:`dispatcher` which essentially loads and executes the desired transform on the client's
machine. A typical execution of a local transform is performed in the following manner in Sploitego:

#. Maltego executes :program:`dispatcher`.
#. :program:`dispatcher` finds and loads the specified local transform module.
#. If successful, :program:`dispatcher` checks for the presence of the :py:func:`dotransform` function in the local
   transform module.
#. Additionally, :program:`dispatcher` checks for the presence of the :py:func:`onterminate` function in the local
   transform module and registers the function as an exit handler if it exists.
#. If :py:func:`dotransform` exists, :program:`dispatcher` calls :py:func:`dotransform` passing in, both, the
   :py:data:`request` and :py:data:`response` objects
#. :py:func:`dotransform` does its thing and returns the :py:data:`response` object to :program:`dispatcher`
#. Finally, :program:`dispatcher` serializes the :py:data:`response` object and returns the result to ``stdout``

In the event that an exception is raised during the execution of a local transform, :program:`dispatcher` will catch the
exception and send an exception message to Maltego's UI. If a local transform is marked to run as the super-user,
:program:`dispatcher` will try to elevate its privilege level using :program:`pysudo` prior to calling
:py:func:`dotransform`.

Available Tools
===============

Sploitego comes with a bunch of useful/interesting scripts for your use:

* :program:`sploitego`: a central commander that provides the functionality in the programs listed below.
* :program:`dispatcher`: alias for ``sploitego run-transform``; loads the specified local transform module and executes
  it, returning its results to Maltego.
* :program:`mtgdebug`: alias for ``sploitego debug-transform``; same as :program:`dispatcher` but used for command-line
  testing of local transform modules.
* :program:`mtginstall`: alias for ``sploitego install-package`` installs and configures local transforms in the
  Maltego UI.
* :program:`mtguninstall`: alias for ``sploitego uninstall-package``; uninstalls and unconfigures local transforms in
  the Maltego UI.
* :program:`mtgsh`: alias for ``sploitego shell``; an interactive shell for running local transforms (work in progress).
* :program:`mtgpkggen`: alias for ``sploitego create-package``; generates a transform package skeleton for eager
  transform developers.
* :program:`mtgtransgen`: alias for ``sploitego create-transform``; generates a transform module and automatically
  adds it to the ``__init__.py`` file.
* :program:`mtgx2csv`: alias for ``sploitego mtgx2csv``; generates a comma-separated report (CSV) of a Maltego-
  generated graph.
* :program:`csv2sheets`: alias for ``sploitego csv2sheets``; separates the CSV report into multiple CSV files containing
  entity types of the same type.

The following subsections describe the tools in detail.

:program:`sploitego` commander
------------------------------

The :program:`sploitego` script is a central commander that provides various kinds of functionality. It accepts the
following parameters:

.. program:: sploitego

.. option:: <command>

    One of the following commands that the :program:`sploitego` commander script will execute:

    * :option:`help` - provides detailed help for each of the following commands
    * :option:`create-package` - Creates a Sploitego transform package skeleton.
    * :option:`create-transform` - Creates a new transform in the specified directory and auto-updates ``__init__.py``.
    * :option:`csv2sheets` - Convert mixed entity type CSVs to separated CSV sheets.
    * :option:`debug-transform` - Runs Sploitego local transforms in a terminal-friendly fashion.
    * :option:`delete-transform` - Deletes a transform in the specified directory and auto-updates ``__init__.py``.
    * :option:`install-package` - Installs and configures sploitego transform packages in Maltego's UI.
    * :option:`list-commands` - Lists all the available sploitego commands.
    * :option:`mtgx2csv` - Convert Maltego graph files (*.mtgx) to comma-separated values (CSV) file.
    * :option:`rename-transform` - Renames a transform in the specified directory and auto-updates ``__init__.py``.
    * :option:`run-transform` - Runs Sploitego local transforms in a terminal-friendly fashion.
    * :option:`shell` - Creates a Sploitego debug shell for the specified transform package.
    * :option:`uninstall-package` - Uninstalls and unconfigures sploitego transform packages in Maltego's UI.

.. option:: [command options]

    Optional command arguments passed to the :program:`sploitego` command. Use ``sploitego help <command>`` to get
    detailed help information on each of the commands above.

The following sub-sections will cover each of the commands in detail.


:option:`help` command
^^^^^^^^^^^^^^^^^^^^^^

The :option:`help` command provides detailed help information for a specific :program:`sploitego` command. It accepts
the following parameters:

.. program:: help

.. option:: <command>

    The name of the :program:`sploitego` command to get help for.

The following command illustrates the use of the :option:`help` command to retrieve command help associated with the
:option:`create-package` command::

    $ sploitego help create-package
    usage: sploitego create-package <package name>

    Creates a Sploitego transform package skeleton.

    positional arguments:
      <package name>  The name of the sploitego package you wish to create.

    optional arguments:
      -h, --help      show this help message and exit


:option:`run-transform` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :option:`run-transform` command loads and executes the specified local transform module and returns transform
results to the Maltego UI (in XML format). It accepts the following parameters:

.. program:: run-transform

.. option:: <transform module>

    The name of the python module that contains the local transform data mining logic (e.g.
    ``sploitego.transforms.nmapfastscan``).

.. option:: [param1 ... paramN]

    Any extra local transform parameters that can be parsed using :py:mod:`optparse` or :py:mod:`argparse` (e.g.
    ``-p 80``).

.. option:: <value>

    The value of the entity being passed into the local transform (e.g. ``google.com``).

.. option:: [field1=value1...#fieldN=valueN]

    optionally, any entity field values delimited by ``#`` (e.g. ``url=http://www.google.ca#public=true``)

The following example illustrates the use of :option:`run-program` to execute the
:py:mod:`sploitego.transforms.nmapfastscan` transform module passing an input entity value of ``www.google.com``::

    $ sploitego run-transform sploitego.transforms.nmapfastscan www.google.com
    <MaltegoMessage><MaltegoTransformResponseMessage><Entities><Entity Type="sploitego.NmapReport"><Value>Nmap -n -F www.google.com Report: Mon Aug 27 21:44:15 2012</Value><Weight>1</Weight><AdditionalFields><Field DisplayName="Report File" MatchingRule="strict" Name="report.file">/Users/foobar/reports/nmap-27082012-21h44m17s.xml</Field><Field DisplayName="Command" MatchingRule="strict" Name="scan.command">/usr/local/bin/nmap -oX - -n -F www.google.com</Field></AdditionalFields></Entity></Entities></MaltegoTransformResponseMessage></MaltegoMessage>


:option:`debug-transform` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :option:`debug-transform` command functions in the same manner as the :option:`run-transform` command except that
its output is terminal friendly. It accepts the following parameters:

.. program:: debug-transform

.. option:: <transform module>

    The name of the python module that contains the local transform data mining logic (e.g.
    ``sploitego.transforms.nmapfastscan``).

.. option:: [param1 ... paramN]

     Any extra local transform parameters that can be parsed using :py:mod:`optparse` or :py:mod:`argparse` (e.g.
     ``-p 80``).

.. option:: <value>

    The value of the entity being passed into the local transform (e.g. ``google.com``).

.. option:: [field1=value1...#fieldN=valueN]

    optionally, any entity field values delimited by ``#`` (e.g. ``url=http://www.google.ca#public=true``)

The following is an example that illustrates running the :py:mod:`sploitego.transforms.nmapfastscan` transform module
with an input entity value of ``www.google.com``::

    $  sploitego debug-transform sploitego.transforms.nmapfastscan www.google.com
      `- MaltegoTransformResponseMessage:
        `- Entities:
          `- Entity:  {'Type': 'sploitego.Port'}
            `- Value: 80
            `- Weight: 1
            `- AdditionalFields:
              `- Field: TCP {'DisplayName': 'Protocol', 'Name': 'protocol', 'MatchingRule': 'strict'}
              `- Field: Open {'DisplayName': 'Port Status', 'Name': 'port.status', 'MatchingRule': 'strict'}
              `- Field: 173.194.75.147 {'DisplayName': 'Destination IP', 'Name': 'ip.destination', 'MatchingRule': 'strict'}
              `- Field: syn-ack {'DisplayName': 'Port Response', 'Name': 'port.response', 'MatchingRule': 'strict'}
            `- IconURL: file:///Library/Python/2.6/site-packages/sploitego-1.0-py2.6.egg/sploitego/resources/images/networking/openport.gif
            `- DisplayInformation:
              `- Label: http {'Type': 'text/text', 'Name': 'Service Name'}
              `- Label: table {'Type': 'text/text', 'Name': 'Method'}
    ...


:option:`install-package` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :option:`install-package` command installs and configures local transforms in the Maltego UI. It accepts the
following parameters:

.. program:: install-package

.. option:: <package>

    Name of the transform package that contains transform modules (i.e. :py:mod:`sploitego`).

.. option:: -s [dir], --settings-dir=[dir]

    The name of the directory that contains Maltego's settings (i.e. ``~/.maltego/<version>`` in Linux,
    ``~/Library/Application\ Support/maltego/<version>`` in Mac OS X).

.. option:: -w [dir], --working-dir=[dir]

    The default working directory for the Maltego transforms.

The following example illustrates the use of :option:`install-package` to install transforms from the `sploitego`
transform package::

    $ sploitego install-package sploitego
    Installing transform sploitego.v2.NmapReportToBanner_Amap from sploitego.transforms.amap...
    Installing transform sploitego.v2.WebsiteToSiteCategory_BlueCoat from sploitego.transforms.bcsitereview...
    Installing transform sploitego.v2.DomainToDNSName_Bing from sploitego.transforms.bingsubdomains...
    Installing transform sploitego.v2.DNSNameToIPv4Address_DNS from sploitego.transforms.dnsalookup...
    Installing transform sploitego.v2.IPv4AddressToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
    Installing transform sploitego.v2.NSRecordToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
    ...


:option:`uninstall-package` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :option:`uninstall-package` command uninstalls and unconfigures all the local transform modules within the specified
transform package in the Maltego UI. It accepts the following parameters:

.. program:: uninstall-package

.. option:: <package>

    The name of the transform package that contains transform modules. (i.e. :py:mod:`sploitego`)

.. option:: -s [dir], --settings-dir=[dir]

    The name of the directory that contains Maltego's settings (i.e. ``~/.maltego/<version>`` in Linux,
    ``~/Library/Application\ Support/maltego/<version>`` in Mac OS X)

The following example illustrates the use of :option:`uninstall-package` to uninstall transforms from the
:py:mod:`sploitego` transform package::

    $ sploitego uninstall-package sploitego
    Multiple versions of Maltego detected:
    [0] Maltego v3.1.1
    [1] Maltego v3.1.1CE
    Please select which version you wish to install the transforms in [0]: 1
    Uninstalling transform sploitego.v2.NmapReportToBanner_Amap from sploitego.transforms.amap...
    Uninstalling transform sploitego.v2.WebsiteToSiteCategory_BlueCoat from sploitego.transforms.bcsitereview...
    Uninstalling transform sploitego.v2.DomainToDNSName_Bing from sploitego.transforms.bingsubdomains...
    Uninstalling transform sploitego.v2.DNSNameToIPv4Address_DNS from sploitego.transforms.dnsalookup...
    Uninstalling transform sploitego.v2.IPv4AddressToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
    Uninstalling transform sploitego.v2.NSRecordToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
    ...


:option:`shell` command
^^^^^^^^^^^^^^^^^^^^^^^

The :option:`shell` command offers an interactive shell for running transforms (work in progress). It accepts the
following parameters:

.. program:: shell

.. option:: <transform package>

    The name of the transform package to load.

The following example illustrates the use of :option:`shell` to run transforms from the :py:mod:`sploitego` transform
package::

    $ sploitego shell sploitego
    Welcome to Sploitego.
    mtg> whatismyip('4.2.2.1')
    `- MaltegoTransformResponseMessage:
      `- Entities:
        `- Entity:  {'Type': 'maltego.IPv4Address'}
          `- Value: 10.0.1.22
          `- Weight: 1
          `- AdditionalFields:
            `- Field: true {'DisplayName': 'Internal', 'Name': 'ipaddress.internal', 'MatchingRule': 'strict'}
            `- Field: 68:a8:6d:4e:0f:72 {'DisplayName': 'Hardware Address', 'Name': 'ethernet.hwaddr', 'MatchingRule': 'strict'}
    mtg>


:option:`create-package` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :option:`create-package` command generates a transform package skeleton for eager transform developers. It accepts
the following parameters:

.. program:: create-package

.. option:: <package name>

    The desired name of the transform package you wish to develop.

The following example illustrates the use of :option:`create-package` to create a transform package named
:py:mod:`mypackage`::

    $ sploitego create-package foobar
    creating skeleton in foobar
    creating directory foobar
    creating directory foobar/src
    creating directory foobar/maltego
    creating directory foobar/src/foobar
    creating directory foobar/src/foobar/transforms
    creating directory foobar/src/foobar/transforms/common
    creating directory foobar/src/foobar/resources
    creating directory foobar/src/foobar/resources/etc
    creating directory foobar/src/foobar/resources/images
    creating file foobar/setup.py...
    creating file foobar/README.md...
    creating file foobar/src/foobar/__init__.py...
    creating file foobar/src/foobar/resources/__init__.py...
    creating file foobar/src/foobar/resources/etc/__init__.py...
    creating file foobar/src/foobar/resources/images/__init__.py...
    creating file foobar/src/foobar/resources/etc/foobar.conf...
    creating file foobar/src/foobar/transforms/__init__.py...
    creating file foobar/src/foobar/transforms/helloworld.py...
    creating file foobar/src/foobar/transforms/common/__init__.py...
    creating file foobar/src/foobar/transforms/common/entities.py...
    done!


:option:`create-transform` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :option:`create-transform` command generates a transform module and automatically adds it to the ``__init__.py``
file in a transform package. It accepts the following parameters:

.. program:: create-transform

.. option:: <transform name>

    The desired name of the transform module to create.

The following example illustrates the use of :option:`create-transform` to create a transform module named
py:mod:`cooltransform`::

    $ cd foobar/src/foobar/transforms/
    $ sploitego create-transform cooltransform
    creating file ./cooltransform.py...
    updating __init__.py
    done!


:option:`rename-transform` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :option:`create-transform` command renames a transform module and automatically adjusts its entry in the
``__init__.py`` file in a transform package. It accepts the following parameters:

.. program:: rename-transform

.. option:: <transform name>

    The name of the transform module to rename.

.. option:: <new transform name>

    The new name of the specified transform module.

The following example illustrates the use of :option:`create-transform` to create a transform module named
py:mod:`cooltransform`::

    $ cd foobar/src/foobar/transforms/
    $ sploitego rename-transform helloworld bye
    renaming transform '/Users/user1/foo/src/foo/transforms/helloworld.py' to '/Users/user1/foo/src/foo/transforms/bye.py'...
    updating /Users/user1/foo/src/foo/transforms/__init__.py
    done!


:option:`delete-transform` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :option:`delete-transform` command deletes a transform module and automatically removes its entry in the
``__init__.py`` file in a transform package. It accepts the following parameters:

.. program:: rename-transform

.. option:: <transform name>

    The name of the transform module to rename.

The following example illustrates the use of :option:`delete-transform` to create a transform module named
py:mod:`bye`::

    $ sploitego delete-transform bye
    deleting transform '/Users/user1/foo/src/foo/transforms/bye.py'...
    updating /Users/user1/foo/src/foo/transforms/__init__.py
    done!


:option:`mtgx2csv` command
^^^^^^^^^^^^^^^^^^^^^^^^^^
The `mtgx2csv` command generates a comma-separated report (CSV) of a Maltego-generated graph. It accepts the following
parameters:

.. program:: mtgx2csv

.. option:: <graph>

    The name of the Maltego graph file.

The following example illustrates the use of :option:`mtgx2csv` command to create a CSV report of a Maltego graph file
named ``Graph1.mtgx``::

    $ sploitego mtgx2csv Graph1.mtgx
    $ ls *.csv
    Graph1.csv


:option:`csv2sheets` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :option:`csv2sheets` command separates the CSV report into multiple CSV files containing entities of the same type.
It accepts the following parameters:

.. program:: csv2sheets

.. option:: <csv report>

    The name of the CSV report generated by the :option:`mtgx2csv` command.

.. option:: <prefix>

    A prefix to prepend to the generated CSV files.

The following example illustrates the use of :option:`csv2sheets` command to create a CSV files containing entities of
the same type from the CSV report ``Graph1.csv``::

    $ sploitego csv2sheets Graph1.csv Test
    $ ls *.csv
    Graph1.csv Test_1.csv Test_2.csv


:option:`list-commands` command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :option:`list-commands` command lists the set of available commands in :program:`sploitego` commander. It accepts no
parameters. The following examples illustrates the execution of :option:`list-commands`::

    $ sploitego list-commands
    create-package - Creates a Sploitego transform package skeleton.
    create-transform - Creates a new transform in the specified directory and auto-updates __init__.py.
    csv2sheets - Convert mixed entity type CSVs to separated CSV sheets.
    debug-transform - Runs Sploitego local transforms in a terminal-friendly fashion.
    delete-transform - Deletes a transform in the specified directory and auto-updates __init__.py.
    install-package - Installs and configures sploitego transform packages in Maltego's UI
    list-commands - Lists all the available sploitego commands
    mtgx2csv - Convert Maltego graph files (*.mtgx) to comma-separated values (CSV) file.
    rename-transform - Renames a transform in the specified directory and auto-updates __init__.py.
    run-transform - Runs Sploitego local transforms in a terminal-friendly fashion.
    shell - Creates a Sploitego debug shell for the specified transform package.
    uninstall-package - Uninstalls and unconfigures sploitego transform packages in Maltego's UI