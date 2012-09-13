####################
Installing Sploitego
####################


Supported Platforms
===================

Sploitego should be cross-platform compatible, however, it has only been tested on the following platforms:

* Mac OS X 10.6+ (MacPorts included).
* Linux.

Testers are very much welcome to provide feedback on their experience with various platforms.

Software Requirements
=====================

Sploitego is only supported on Python version **2.6**. The setup script will automatically download and install most of
the prerequisite modules, however, some modules will still need to be installed manually. The following modules require
manual installation:

* **Scapy 2.1.0:** See the `Scapy Installation Manual <http://www.secdev.org/projects/scapy/doc/installation.html>`_
  for more details for build instructions pertaining to your operating system.
* **sip & PyQt4:** `Download <http://www.riverbankcomputing.co.uk/software/pyqt/download/>`_
* **easygui:** `Download <http://easygui.sourceforge.net/download/index.html>`_

Some of the transforms require external command-line tools (e.g. :program:`nmap`, :program:`amap`, :program:`p0f`, etc).
The following command-line tools are currently supported:

* **Nmap version 5 or later:** `Download <http://nmap.org/download.html>`_
* **P0f version 3.05b:** `Download <http://lcamtuf.coredump.cx/p0f3/releases/p0f-3.05b.tgz>`_
* **Amap version 5.4:** `Download <http://www.thc.org/releases/amap-5.4.tar.gz>`_
* **Metasploit:** `Download <http://downloads.metasploit.com/data/releases/framework-latest.tar.bz2>`_
* **Nessus:** `Download <http://www.tenable.com/products/nessus/nessus-product-overview>`_

Installation
============

Once you've installed the necessary prerequisites, installing Sploitego is a cinch. Just run:

.. code-block:: bash

    $ sudo python setup.py install

This will install all the necessary modules and download any dependencies (other than what's required above)
automatically. Once Sploitego has been installed, it's time to install the transforms. First, make sure Maltego has been
run for the first time and initialized (i.e. logged in, transforms discovered, etc.). Once initialized, shutdown Maltego
and run the following command:

.. code-block:: bash

    $ sploitego install-package sploitego

If the :program:`sploitego` script is not in your PATH you may need to perform some additional steps
(see :ref:`known-issues`). The :program:`sploitego install-package` command will automatically find the Maltego settings
directory and install and configure the transforms in Maltego's UI. If multiple versions of Maltego are found on your
system, the installer will ask you which version of Maltego you wish to install the local transforms in. In the odd case
where :program:`sploitego install-package` is not able to determine where your Maltego settings directory is, you can
specify it using the :option:`-s` parameter.

The Maltego settings directory is the directory where Maltego's current configuration state is held. This is typically
in:

* **Mac OS X:** ``~/Library/Application\ Support/maltego/<Maltego Version>`` (e.g.
  ``~/Library/Application\ Support/maltego/3.1.1`` for Maltego 3.1.1)
* **Linux:** ``~/.maltego/<Maltego Version>`` (e.g. ``~/.maltego/3.1.1CE`` for Maltego 3.1.1 CE)
* **Windows:** ``%APPDATA%/.maltego/<Maltego Version>`` (e.g. ``%APPDATA%/.maltego/3.1.1`` for Maltego 3.1.1)

:program:`sploitego install-package` also accepts an additional :option:`-w` parameter which can be used to specify the
working directory that you wish to use as a scratchpad for your transforms. This is also the directory where you can
specify any additional configuration options to override certain settings for transforms. If you're unsure, you may
exclude the parameter and :program:`sploitego install-package` will use your current working directory. For example::

    $ pwd
    /home/user1
    $ sploitego install sploitego

Will install the transforms located in the :py:mod:`sploitego.transforms` python package to the Maltego settings
directory with a working path of the user's home director (``~/``). **WARNING:** DO NOT use :program:`sudo` for
:program:`sploitego install-package`. Otherwise, you'll pooch your Maltego settings directory and Maltego will not be
able to run or find any additional transforms.

If successful, you will see the following output in your terminal::

    $ sploitego install sploitego
    Installing transform sploitego.v2.NmapReportToBanner_Amap from sploitego.transforms.amap...
    Installing transform sploitego.v2.WebsiteToSiteCategory_BlueCoat from sploitego.transforms.bcsitereview...
    Installing transform sploitego.v2.DomainToDNSName_Bing from sploitego.transforms.bingsubdomains...
    Installing transform sploitego.v2.DNSNameToIPv4Address_DNS from sploitego.transforms.dnsalookup...
    Installing transform sploitego.v2.IPv4AddressToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
    Installing transform sploitego.v2.NSRecordToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
    ...

In addition you should see ``sploitego.conf`` copied to your working directory. You'll probably want to go through it
and take a look at the various options you can override for each of the transforms.

Additional Steps
================

Entities
--------

You will need to import the custom entity definition file manually via Maltego's UI. The entity definition file can be
located in the ``maltego/`` directory of the Sploitego distribution. To install the entities:

#. Run Maltego;
#. In Maltego, navigate to the ``Manage`` tab;
#. Click on the ``Import Entities`` button;
#. Select the ``maltego/entities.mtz`` file in the file browser dialog and click ``Next`` to completion.

API Keys
--------

Some of the transforms in Sploitego require additional configuration in order to operate correctly. The following web
API keys are required:

* **Bing API:** `Sign up <https://datamarket.azure.com/dataset/5BA839F1-12CE-4CCE-BF57-A49D98D29A44>`_
* **Bluecoat K9:** `Sign up <http://www1.k9webprotection.com/get-k9-web-protection-free>`_ (download not required)
* **Pipl:** `Sign up <http://dev.pipl.com/>`_

To configure these options edit ``sploitego.conf`` from your transform's working directory specified during
:program:`sploitego install-package` and override the necessary settings in the configuration file with your desired
values. Place-holders encapsulated with angled brackets (``<``, ``>``) can be found throughout the configuration file
where additional configuration is required.
