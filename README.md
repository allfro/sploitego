Sploitego - Maltego's (Local) Partner in Crime
==================================================

## 1.0 - Introduction

Sploitego is a **rapid** local transform development framework for [Maltego](http://paterva.com/) written in Python. Sploitego's core
features include:

- An easily **extensible and configurable** framework;
- A set of **powerful** and **easy-to-use** scripts for debugging, configuring, and installing transforms;
- A **plethora** of auxiliary modules focused on [Open Source Intelligence (OSINT)](http://en.wikipedia.org/wiki/Open-source_intelligence)
  gathering as well as **penetration testing**;
- Finally, a great number of **really awesome pen-testing transforms**.

The original focus of Sploitego was to provide a set of transforms that would aid in the execution of penetration tests,
and vulnerability assessments. Ever since it's first prototype, it has become evident that the framework can be used for
much more than that. Sploitego is perfect for anyone wishing to graphically represent their data in [Maltego](http://paterva.com) without
the hassle of learning a whole bunch of unnecessary stuff. It has generated interest from digital forensics analysts to
pen-testers, and even [psychologists](http://www.forbes.com/sites/kashmirhill/2012/07/20/using-twitter-to-help-expose-psychopaths).

### 1.1 - Terminology

Before we get started with the documentation, it might be useful to introduce some of the terminology that will be used
throughout the documentation:

* **Transform Module**: a python module local transform code.
* **Transform Package**: a python package containing one or more transform modules.
* **TODO**

## 2.0 - Why Use Sploitego?

### 2.1 - Extensibility
To develop *local* transforms for Maltego with *ease*; no need to learn XML, the local transform 
[specification](http://paterva.com/web5/documentation/localtransforms.php), or develop tedious routines for command-line input parsing, 
debugging, or XML messaging. All you need to do is focus on developing the core data mining logic and Sploitego does the rest. Sploitego's 
interface is designed on the principles of [convention over configuration](http://en.wikipedia.org/wiki/Convention_over_configuration) and 
[KISS](http://en.wikipedia.org/wiki/KISS_principle).

For example, this is what a local transform looks like using Sploitego:

```python
#!/usr/bin/env python

from sploitego.maltego.message import Phrase

def dotransform(request, response):
    response += Phrase('Hello %s' % request.value)
    return response
```

And this is what a custom-defined entity looks like:

```python
class MyEntity(Entity):
    pass
```

If you're already excited about using Sploitego, wait until you see the other features it has to offer!

## 3.0 - Installing Sploitego

### 3.1 - Supported Platforms
Sploitego has currently been tested on Mac OS X Snow Leopard and Lion (without MacPorts). However, the framework is
theoretically cross-platform compatible. Testers are very much welcome to provide feedback on their experience with
various platforms.

### 3.2 - Requirements
Sploitego is only supported on Python version 2.6. The setup script will automatically download and install most of the
prerequisite modules, however, some modules will still need to be installed manually. The following modules require
manual installation:
* **Scapy 2.1.0**: See the [Scapy Installation Manual for more details](http://www.secdev.org/projects/scapy/doc/installation.html)
  for build instructions pertaining to your operating system.
* **sip & PyQt4**: [Download](http://www.riverbankcomputing.co.uk/software/pyqt/download/)
* **easygui**: [Download](http://easygui.sourceforge.net/download/index.html)

Some of the transforms require external command-line tools (e.g. nmap, amap, p0f, etc.). The following command-line
tools are currently supported:
* **Nmap version 5.51**: [Download](http://nmap.org/dist/?C=M&O=D)
* **P0f version 3.05b**: [Download](http://lcamtuf.coredump.cx/p0f3/releases/p0f-3.05b.tgz)
* **Amap version 5.4**: [Download](http://www.thc.org/releases/amap-5.4.tar.gz)
* **Metasploit**: [Download](http://downloads.metasploit.com/data/releases/framework-latest.tar.bz2)
* **Nessus**: [Download](http://www.tenable.com/products/nessus/nessus-product-overview)

### 3.3 - Installation
Once you've installed the necessary prerequisites, installing Sploitego is a cinch. Just run:

```bash
$ sudo python setup.py install
```

This will install all the necessary modules and download any dependencies (other than libdnet and PyQt4) automatically.
Once Sploitego has been installed, it's time to install the transforms. First, make sure Maltego is not running. Second,
make sure the Sploitego scripts are in your path. When you're ready, run the following command:

```bash
$ mtginstall -p sploitego.transform -m <Maltego Settings Dir> -w <Transforms Working Dir>
```

```<Maltego Settings Dir>``` is the directory where Maltego's current configuration state is held. This is typically in:

* **Mac OS X**: ```~/Library/Application\ Support/maltego/<Maltego Version>```
  (e.g. ```~/Library/Application\ Support/maltego/3.1.1``` for Maltego 3.1.1)
* **Linux**: Unknown (TODO: need testers)
* **Windows**: Unknown (TODO: need testers)

```<Transforms Working Dir>``` is the working directory that you wish to use as a scratchpad for your transforms. This is
also the directory where you can specify an additional configuration file to override certain settings for transforms.
If you're unsure, pick your home directory (e.g. ```~/```).

For example:

```bash
$ mtginstall -p sploitego.transforms -m  ~/Library/Application\ Support/maltego/3.1.1 -w ~/
```

Will install the transforms located in the ```sploitego.transforms``` python package in the Maltego 3.1.1 settings
directory with a working path of the user's home director (```~/```). **WARNING**: DO NOT use ```sudo``` for
```mtginstall```. Otherwise, you'll pooch your Maltego settings directory and Maltego will not be able to run or find
any additional transforms.

If successful, you will see the following output in your terminal:

```bash
$ mtginstall -w ~/ -p sploitego.transforms -m ~/Library/Application\ Support/maltego/v3.1.1
Installing transform sploitego.v2.NmapReportToBanner_Amap from sploitego.transforms.amap...
Installing transform sploitego.v2.WebsiteToSiteCategory_BlueCoat from sploitego.transforms.bcsitereview...
Installing transform sploitego.v2.DomainToDNSName_Bing from sploitego.transforms.bingsubdomains...
Installing transform sploitego.v2.DNSNameToIPv4Address_DNS from sploitego.transforms.dnsalookup...
Installing transform sploitego.v2.IPv4AddressToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
Installing transform sploitego.v2.NSRecordToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
...
```

### 3.4 - Additional Steps
Some of the transforms in Sploitego require additional configuration in order to operate correctly. The following web API 
keys are required:
* Bing API: [Sign up](https://datamarket.azure.com/dataset/5BA839F1-12CE-4CCE-BF57-A49D98D29A44)
* Bluecoat K9: [Sign up](http://www1.k9webprotection.com/get-k9-web-protection-free) (download not required)
* Pipl: [Sign up](http://dev.pipl.com/)

To configure these options copy ```sploitego.conf``` from the ```src/sploitego/resources/etc/``` in your build directory
into the transform working directory specified during mtginstall (i.e. ```<Transform Working Dir>```) and override the
necessary settings in the configuration file with your desired values. Place-holders encapsulated with angled brackets 
(```<```, ```>```) can be found throughout the configuration file where additional configuration is required.


## 4.0 - Framework Overview

### 4.1 - Sploitego Local Transform Execution
Local transforms in Maltego execute on the client's local machine by executing a local script or executable and listening
for results on ```stdout``` (or standard output). Sploitego provides a single script for local transform execution called
```dispatcher``` which essentially determines which transform to execute on the client's machine. A typical local transform
is executed in the following manner in Sploitego:

1. Maltego executes ```dispatcher```.
3. If successful, ```dispatcher``` checks for the presence of the ```dotransform``` function in the local transform module.
4. Additionally, ```dispatcher``` checks for the presence of the ```onterminate``` function in the local transform module
   and registers the function as an exit handler if it exists.
5. If ```dotransform``` exists, ```dispatcher``` calls ```dotransform``` passing in, both, the ```request``` and ```response``` 
   objects
6. ```dotransform``` does its thing and returns the ```response``` object to ```dispatcher```
7. Finally, ```dotransform``` serializes the ```response``` object and returns the result to ```stdout```

In the event that an exception is raised during the execution of a local transform, ```dispatcher``` will catch the exception 
and send an exception message to Maltego's UI. If a local transform is marked to run as the super-user, ```dispatcher```
will try to elevate its privilege level using ```pysetuid``` prior to calling ```dotransform```.

### 4.2 - Available Tools
Sploitego comes with a bunch of useful/interesting scripts for your use:

* ```dispatcher```:     loads the specified local transform module and executes it, returning its results to Maltego.
* ```mtgdebug```:       same as dispatcher but used for command-line testing of local transform modules.
* ```mtginstall```:     installs and configures local transforms in the Maltego UI.
* ```mtguninstall```:   uninstall and unconfigures local transforms in the Maltego UI.
* ```mtgsh```:          an interactive shell for running transforms (work in progress).
* ```mtgpkggen```:      generates a transform package skeleton for eager transform developers.
* ```mtgtransgen```:    generates a transform module and automatically adds it to the ```__init__.py``` file.
* ```mtgx2csv```:       generates a comma-separated report (CSV) of a Maltego-generated graph.
* ```csv2sheets```:     separates the CSV report into multiple CSV files containing entity types of the same type.

The following subsections describe the tools in detail.

#### 4.2.1 - ```dispatcher```/```mtgdebug``` commands
The ```dispatcher``` and ```mtgdebug``` scripts loads the specified local transform module and executes it, returning
their results to Maltego or the terminal, respectively. They accept the following parameters:

  * ```<transform module>``` (**required**): the name of the python module that contains the local transform data mining
    logic (e.g. ```sploitego.transforms.nmapfastscan```)
  * ```[param1 ... paramN]``` (**optional**): any extra local transform parameters that can be parsed using ```optparse```
    (e.g. ```-p 80```)
  * ```<value>``` (**required**): the value of the entity being passed into the local transform (e.g. ```google.com```)
  * ```[field1=value1...#fieldN=valueN]``` (**optional**): optionally, any entity field values delimited by ```#``` (e.g.
    ```url=http://www.google.ca#public=true```)

The following example illustrates the use of ```mtgdebug``` to execute the ```sploitego.transforms.nmapfastscan```
transform module on ```www.google.com```:

```bash
$  mtgdebug sploitego.transforms.nmapfastscan www.google.com
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
```

#### 4.2.2 - ```mtginstall``` command
The ```mtginstall``` script installs and configures local transforms in the Maltego UI. It accepts the following
parameters:

* ```-h```, ```--help```: shows help
* ```-p <package>, --package=<package>``` (**required**): name of the transform package that contains transform modules. (i.e.
  sploitego.transforms)
* ```-m <prefix>```, ```--maltego-settings-prefix=<prefix>``` (**required**): the name of the directory that contains Maltego's
  settings (i.e. ```~/.maltego/<version>``` in Linux, ```~/Library/Application\ Support/maltego/<version>``` in Mac OS X)
* ```-w <dir>, --working-dir=<dir>``` (**required**): the default working directory for the Maltego transforms

The following example illustrates the use of ```mtginstall``` to install transforms from the ```sploitego.transforms```
transform package:

```bash
$ mtginstall -w ~/ -p sploitego.transforms -m ~/Library/Application\ Support/maltego/v3.1.1
Installing transform sploitego.v2.NmapReportToBanner_Amap from sploitego.transforms.amap...
Installing transform sploitego.v2.WebsiteToSiteCategory_BlueCoat from sploitego.transforms.bcsitereview...
Installing transform sploitego.v2.DomainToDNSName_Bing from sploitego.transforms.bingsubdomains...
Installing transform sploitego.v2.DNSNameToIPv4Address_DNS from sploitego.transforms.dnsalookup...
Installing transform sploitego.v2.IPv4AddressToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
Installing transform sploitego.v2.NSRecordToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
...
```

#### 4.2.3 - ```mtguninstall``` command
The ```mtguninstall``` script uninstalls and unconfigures all the local transform modules within the specified transform
package in the Maltego UI. It accepts the following parameters:

* ```-h```, ```--help```: shows help
* ```-p <package>, --package=<package>``` (**required**): name of the transform package that contains transform modules. (i.e.
  sploitego.transforms)
* ```-m <prefix>```, ```--maltego-settings-prefix=<prefix>``` (**required**): the name of the directory that contains Maltego's
  settings (i.e. ```~/.maltego/<version>``` in Linux, ```~/Library/Application\ Support/maltego/<version>``` in Mac OS X)

The following example illustrates the use of ```mtguninstall``` to uninstall transforms from the ```sploitego.transforms```
transform package:

```bash
$ mtguninstall -p sploitego.transforms -m ~/Library/Application\ Support/maltego/v3.1.1
```

#### 4.2.4 - ```mtgsh``` command
The ```mtgsh``` script offers an interactive shell for running transforms (work in progress). It accepts the following
parameters:

* ```<transform package>``` (**required**): the name of the transform package to load.

The following example illustrates the use of ```mtgsh``` to run transforms from the ```sploitego.transforms```
transform package:

```bash
$ mtgsh sploitego.transforms
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
```


#### 4.2.5 - ```mtgpkggen``` command
The ```mtgpkggen``` script generates a transform package skeleton for eager transform developers. It accepts the following
parameters:

* ```<package name>``` (**required**): the desired name of the transform package you wish to develop.

The following example illustrates the use of ```mtgpkggen``` to create a transform package named ```mypackage```:

```bash
$ mtgpkggen mypackage
creating skeleton in mypackage
creating file setup.py...
creating file README.md...
creating file src/mypackage/transforms/common/entities.py...
creating file src/mypackage/transforms/helloworld.py...
creating file src/mypackage/__init__.py...
creating file src/mypackage/transforms/__init__.py...
creating file src/mypackage/transforms/common/__init__.py...
done!
```


#### 4.2.6 - ```mtgtransgen``` command
The ```mtgtransgen``` generates a transform module and automatically adds it to the ```__init__.py``` file in a
transform package. It accepts the following parameters:

* ```<transform name>``` (**required**): the desired name of the transform module to create.

The following example illustrates the use of ```mtgtransgen``` to create a transform module named ```cooltransform```:

```bash
$ cd mypackage/src/mypackage/transforms/
$ mtgtransgen cooltransform
creating file ./cooltransform.py...
installing to __init__.py
done!
```

#### 4.2.7 - ```mtgx2csv``` command
The ```mtgx2csv``` script generates a comma-separated report (CSV) of a Maltego-generated graph. It accepts the following
parameters:

* ```<graph>``` (**required**): the name of the Maltego graph file.

The following example illustrates the use of ```mtgx2csv``` to create a CSV report of a Maltego graph file named ```Graph1.mtgx```:

```bash
$ mtgx2csv Graph1.mtgx
```


#### 4.2.8 - ```csv2sheets``` command
The ```csv2sheets``` file separates the CSV report into multiple CSV files containing entities of the same type. It
accepts the following parameters:

* ```<csv report>``` (**required**): the name of the CSV report generated by ```mtgx2csv```
* ```<prefix>``` (**required**): a prefix to prepend to the generated CSV files.

The following example illustrates the use of ```csv2sheets``` to create a CSV files containing entities of the same type
from the CSV report ```Graph1.csv```:

```bash
$ csv2sheets Graph1.csv
```


# Known Issues

## ```dispatcher``` exit code 1

This issue occurs when the Sploitego scripts are not in the system path of the JVM. To fix this issue you will need to
create symlinks to the Sploitego scripts in one of the directories in your path. Unfortunately, it is not as simple as
adding the directory to your $PATH variable. For some reason JVM determines its PATH in a different way than ```bash```,
```csh```, etc. The ```JavaPathChecker``` in ```maltego/JavaPathChecker``` was developed to assist in determining what
directories in the JVM's executable path exist. To run it, just do:

```bash
$ cd maltego/JavaPathChecker
$ python run.py
/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/opt/local/bin
```

Once you receive the output from ```JavaPathChecker``` you'll have to manually add symlinks to each of the Sploitego
scripts in one of the executable directories.


