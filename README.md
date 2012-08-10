Sploitego - Maltego's (Local) Partner in Crime
==============================================

## 1.0 - Introduction

Sploitego is a **rapid** local transform development framework for [Maltego](http://paterva.com/) written in Python.
The original focus of Sploitego was to provide a set of transforms that would aid in the execution of penetration tests,
and vulnerability assessments. Ever since it's first prototype, it has become evident that the framework can be used for
much more than that. Sploitego is perfect for anyone wishing to graphically represent their data in
[Maltego](http://paterva.com) without the hassle of learning a whole bunch of unnecessary stuff. It has generated
interest from digital forensics analysts to pen-testers, and even
[psychologists](http://www.forbes.com/sites/kashmirhill/2012/07/20/using-twitter-to-help-expose-psychopaths).
Sploitego's core features include:

* An easily **extensible and configurable** framework that promotes **maximum reusability**;
* A set of **powerful** and **easy-to-use** scripts for debugging, configuring, and installing transforms;
* A **plethora** of auxiliary modules focused on
  [Open Source Intelligence (OSINT)](http://en.wikipedia.org/wiki/Open-source_intelligence) gathering as well as
  **penetration testing**;
* Finally, a great number of **really awesome pen-testing transforms**.

### 1.1 - Terminology

Before we get started with the documentation, it might be useful to introduce some of the terminology that will be used
throughout the documentation:

* **Entity**: a piece of information on a Maltego graph represented as a node.
* **Transform**: a function that takes one entity as input and produces zero or more entities as output.
* **Input Entity**: the entity that is being passed into the transform to use for data mining purposes.
* **Output Entity**: the entity that is being returned by the transform to be drawn on a Maltego graph.
* **Transform Module**: a python module local transform code.
* **Transform Package**: a python package containing one or more transform modules.

## 2.0 - Why Use Sploitego?

To develop *local* transforms for Maltego with *ease*; no need to learn XML, the local transform 
[specification](http://paterva.com/web5/documentation/localtransforms.php), or develop tedious routines for command-line
input parsing, debugging, or XML messaging. All you need to do is focus on developing the core data mining logic and
Sploitego does the rest. Sploitego's interface is designed on the principles of
[convention over configuration](http://en.wikipedia.org/wiki/Convention_over_configuration) and
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
* **Scapy 2.1.0**: See the
  [Scapy Installation Manual for more details](http://www.secdev.org/projects/scapy/doc/installation.html) for build
  instructions pertaining to your operating system.
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

This will install all the necessary modules and download any dependencies (other than what's required above)
automatically. Once Sploitego has been installed, it's time to install the transforms. First, make sure Maltego has been
run for the first time and initialized (i.e. logged in, transforms discovered, etc.). Once initialized, shutdown Maltego
and run the following command:

```bash
$ mtginstall sploitego
```

If `mtginstall` is not in your PATH you may need to perform some additional steps (see "Known Issues" at the end of
this document. The `mtginstall` script will automatically find the Maltego settings directory and install and
configure the transforms in Maltego's UI. If multiple versions of Maltego our found on your system, the installer will
ask you which version of Maltego you wish to install the local transforms in. In the odd case where `mtginstall` is
not able to determine where your Maltego settings directory is, you can specify the `-s <Maltego Settings Directory>`
parameter.

`<Maltego Settings Dir>` is the directory where Maltego's current configuration state is held. This is typically in:

* **Mac OS X**: `~/Library/Application\ Support/maltego/<Maltego Version>`
  (e.g. `~/Library/Application\ Support/maltego/3.1.1` for Maltego 3.1.1)
* **Linux**: `~/.maltego/<Maltego Version>` (e.g. `~/.maltego/3.1.1CE` for Maltego 3.1.1 CE)
* **Windows**: `%APPDATA%/.maltego/<Maltego Version>` (e.g. `%APPDATA%/.maltego/3.1.1` for Maltego 3.1.1)

`mtginstall` also accepts an additional `-w <Transforms Working Directory>` parameter which specifies the
working directory that you wish to use as a scratchpad for your transforms. This is also the directory where you can
specify any additional configuration options to override certain settings for transforms. If you're unsure, you may
exclude the parameter and `mtginstall` will use your home directory (e.g. `~/`).

For example:

```bash
$ pwd
/home/user1
$ mtginstall sploitego
```

Will install the transforms located in the `sploitego.transforms` python package in the Maltego settings directory
with a working path of the user's home director (`~/`). **WARNING**: DO NOT use `sudo` for `mtginstall`. Otherwise,
you'll pooch your Maltego settings directory and Maltego will not be able to run or find any additional transforms.

If successful, you will see the following output in your terminal:

```bash
$ mtginstall sploitego
Installing transform sploitego.v2.NmapReportToBanner_Amap from sploitego.transforms.amap...
Installing transform sploitego.v2.WebsiteToSiteCategory_BlueCoat from sploitego.transforms.bcsitereview...
Installing transform sploitego.v2.DomainToDNSName_Bing from sploitego.transforms.bingsubdomains...
Installing transform sploitego.v2.DNSNameToIPv4Address_DNS from sploitego.transforms.dnsalookup...
Installing transform sploitego.v2.IPv4AddressToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
Installing transform sploitego.v2.NSRecordToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
...
```

In addition you should see `sploitego.conf` copied to your working directory. You'll probably want to go through it and
take a look at the various options you can override for each of the transforms.

### 3.4 - Additional Steps
Some of the transforms in Sploitego require additional configuration in order to operate correctly. The following web
API keys are required:
* Bing API: [Sign up](https://datamarket.azure.com/dataset/5BA839F1-12CE-4CCE-BF57-A49D98D29A44)
* Bluecoat K9: [Sign up](http://www1.k9webprotection.com/get-k9-web-protection-free) (download not required)
* Pipl: [Sign up](http://dev.pipl.com/)

To configure these options edit `sploitego.conf` from your transform's working directory specified during mtginstall
(i.e. ```<Transform Working Dir>```) and override the necessary settings in the configuration file with your desired
values. Place-holders encapsulated with angled brackets (`<`, `>`) can be found throughout the configuration file where
additional configuration is required.


## 4.0 - Framework Overview

### 4.1 - Sploitego Local Transform Execution
Local transforms in Maltego execute on the client's local machine by executing a local script or executable and listening
for results on `stdout` (or standard output). Sploitego provides a single script for local transform execution called
`dispatcher` which essentially loads and executes the desired transform on the client's machine. A typical execution of
a local transform is performed in the following manner in Sploitego:

1. Maltego executes `dispatcher`.
3. If successful, `dispatcher` checks for the presence of the `dotransform` function in the local transform module.
4. Additionally, `dispatcher` checks for the presence of the `onterminate` function in the local transform module and
   registers the function as an exit handler if it exists.
5. If `dotransform` exists, `dispatcher` calls `dotransform` passing in, both, the `request` and `response` objects
6. `dotransform` does its thing and returns the `response` object to `dispatcher`
7. Finally, `dispatcher` serializes the `response` object and returns the result to `stdout`

In the event that an exception is raised during the execution of a local transform, `dispatcher` will catch the
exception and send an exception message to Maltego's UI. If a local transform is marked to run as the super-user,
`dispatcher` will try to elevate its privilege level using `pysudo` prior to calling `dotransform`.

### 4.2 - Available Tools
Sploitego comes with a bunch of useful/interesting scripts for your use:

* `sploitego`:      a central commander that provides the functionality below.
* `dispatcher`:     loads the specified local transform module and executes it, returning its results to Maltego.
* `mtgdebug`:       same as dispatcher but used for command-line testing of local transform modules.
* `mtginstall`:     installs and configures local transforms in the Maltego UI.
* `mtguninstall`:   uninstall and unconfigures local transforms in the Maltego UI.
* `mtgsh`:          an interactive shell for running transforms (work in progress).
* `mtgpkggen`:      generates a transform package skeleton for eager transform developers.
* `mtgtransgen`:    generates a transform module and automatically adds it to the `__init__.py` file.
* `mtgx2csv`:       generates a comma-separated report (CSV) of a Maltego-generated graph.
* `csv2sheets`:     separates the CSV report into multiple CSV files containing entity types of the same type.

The following subsections describe the tools in detail.

#### 4.2.1 - `dispatcher`/`mtgdebug` commands
The `dispatcher` and `mtgdebug` scripts load and execute the specified local transform module, returning transform
results to the Maltego UI or the terminal, respectively. They accept the following parameters:

* `<transform module>` (**required**): the name of the python module that contains the local transform data mining
  logic (e.g. `sploitego.transforms.nmapfastscan`)
* `[param1 ... paramN]` (**optional**): any extra local transform parameters that can be parsed using `optparse`
  (e.g. `-p 80`)
* `<value>` (**required**): the value of the entity being passed into the local transform (e.g. `google.com`)
* `[field1=value1...#fieldN=valueN]` (**optional**): optionally, any entity field values delimited by `#` (e.g.
  `url=http://www.google.ca#public=true`)

The following example illustrates the use of `mtgdebug` to execute the `sploitego.transforms.nmapfastscan` transform
module on `www.google.com`:

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

#### 4.2.2 - `mtginstall` command
The `mtginstall` script installs and configures local transforms in the Maltego UI. It accepts the following
parameters:

* `-h`, `--help`: shows help
* `<package>` (**required**): name of the transform package that contains transform modules (i.e. `sploitego`).
* `-s [dir]`, `--settings-dir=[dir]` (**optional**): the name of the directory that contains Maltego's settings (i.e.
  `~/.maltego/<version>` in Linux, `~/Library/Application\ Support/maltego/<version>` in Mac OS X)
* `-w [dir], --working-dir=[dir]` (**optional, default: current working directory**): the default working directory for
  the Maltego transforms

The following example illustrates the use of `mtginstall` to install transforms from the `sploitego` transform package:

```bash
$ mtginstall sploitego
Installing transform sploitego.v2.NmapReportToBanner_Amap from sploitego.transforms.amap...
Installing transform sploitego.v2.WebsiteToSiteCategory_BlueCoat from sploitego.transforms.bcsitereview...
Installing transform sploitego.v2.DomainToDNSName_Bing from sploitego.transforms.bingsubdomains...
Installing transform sploitego.v2.DNSNameToIPv4Address_DNS from sploitego.transforms.dnsalookup...
Installing transform sploitego.v2.IPv4AddressToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
Installing transform sploitego.v2.NSRecordToDNSName_CacheSnoop from sploitego.transforms.dnscachesnoop...
...
```

#### 4.2.3 - `mtguninstall` command
The `mtguninstall` script uninstalls and unconfigures all the local transform modules within the specified transform
package in the Maltego UI. It accepts the following parameters:

* `-h`, `--help`: shows help
* `<package>` (**required**): name of the transform package that contains transform modules. (i.e. `sploitego`)
* `-s [dir]`, `--settings-dir=[dir]` (**optional**): the name of the directory that contains Maltego's settings (i.e.
  `~/.maltego/<version>` in Linux, `~/Library/Application\ Support/maltego/<version>` in Mac OS X)

The following example illustrates the use of `mtguninstall` to uninstall transforms from the `sploitego` transform
package:

```bash
$ mtguninstall sploitego
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
```

#### 4.2.4 - `mtgsh` command
The `mtgsh` script offers an interactive shell for running transforms (work in progress). It accepts the following
parameters:

* `<transform package>` (**required**): the name of the transform package to load.

The following example illustrates the use of `mtgsh` to run transforms from the `sploitego` transform package:

```bash
$ mtgsh sploitego
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


#### 4.2.5 - `mtgpkggen` command
The `mtgpkggen` script generates a transform package skeleton for eager transform developers. It accepts the following
parameters:

* `<package name>` (**required**): the desired name of the transform package you wish to develop.

The following example illustrates the use of `mtgpkggen` to create a transform package named `mypackage`:

```bash
$ mtgpkggen foobar
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
```


#### 4.2.6 - `mtgtransgen` command
The `mtgtransgen` generates a transform module and automatically adds it to the `__init__.py` file in a transform
package. It accepts the following parameters:

* `<transform name>` (**required**): the desired name of the transform module to create.

The following example illustrates the use of `mtgtransgen` to create a transform module named `cooltransform`:

```bash
$ cd foobar/src/foobar/transforms/
$ mtgtransgen cooltransform
creating file ./cooltransform.py...
updating __init__.py
done!
```

#### 4.2.7 - `mtgx2csv` command
The `mtgx2csv` script generates a comma-separated report (CSV) of a Maltego-generated graph. It accepts the following
parameters:

* `<graph>` (**required**): the name of the Maltego graph file.

The following example illustrates the use of `mtgx2csv` to create a CSV report of a Maltego graph file named
`Graph1.mtgx`:

```bash
$ mtgx2csv Graph1.mtgx
```


#### 4.2.8 - `csv2sheets` command
The `csv2sheets` file separates the CSV report into multiple CSV files containing entities of the same type. It accepts
the following parameters:

* `<csv report>` (**required**): the name of the CSV report generated by `mtgx2csv`
* `<prefix>` (**required**): a prefix to prepend to the generated CSV files.

The following example illustrates the use of `csv2sheets` to create a CSV files containing entities of the same type
from the CSV report `Graph1.csv`:

```bash
$ csv2sheets Graph1.csv IRS
```


### 4.3 - Transform Development Quickstart

The following sections will give you a quick-start tutorial on how to develop transforms.

#### 4.3.1 - Creating a Transform Package
Developing transforms is now easier than ever. If you want to create a whole bunch of transforms or if you wish to take
advantage of `mtginstall` then you'll want to create a transform package. Otherwise, you'll have to manually install
and configure your local transform in the Maltego UI. We'll just go ahead and create a transform package called
`mypackage` because I have a good feeling you'll be really eager to create a whole bunch of transforms:

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

You'll notice that a simple skeleton project was generated, with a `helloworld` transform to get you started. You can
test the `helloworld` transform module by running `sploitego debug-transform` like so:

```bash
$ sploitego debug-transform mypackage.transforms.helloworld Phil
%50
D:This was pointless!
%100
`- MaltegoTransformResponseMessage:
  `- Entities:
    `- Entity:  {'Type': 'test.MyTestEntity'}
      `- Value: Hello Phil!
      `- Weight: 1
      `- AdditionalFields:
        `- Field: 2 {'DisplayName': 'Field 1', 'Name': 'test.field1', 'MatchingRule': 'strict'}
        `- Field: test {'DisplayName': 'Field N', 'Name': 'test.fieldN', 'MatchingRule': 'strict'}
```


#### 4.3.2 - Developing a Transform
Let's take a look at an abbreviated version of  `src/mypackage/transforms/helloworld.py`, from our example above,
to see how this transform was put together.

```python
#!/usr/bin/env python

from sploitego.maltego.message import Person
from sploitego.maltego.utils import debug, progress
from sploitego.framework import configure #, superuser
from common.entities import MypackageEntity

# ...
#@superuser
@configure(
    label='To MypackageEntity [Hello World]',
    description='Returns a MyPackageEntity entity with the phrase "Hello Word!"',
    uuids=[ 'mypackage.v2.MyPackageEntityToPhrase_HelloWorld' ],
    inputs=[ ( 'MyPackageEntity', Person ) ],
    debug=True
)
def dotransform(request, response):
    # Report transform progress
    progress(50)
    # Send a debugging message to the Maltego UI console
    debug('This was pointless!')

    # Create MyPackageEntity entity with value set to 'Hello <request.value>!'
    e = MypackageEntity('Hello %s!' % request.value)

    # Setting field values on the entity
    e.field1 = 2
    e.fieldN = 'test'

    # Update progress
    progress(100)

    # Add entity to response object
    response += e

    # Return response for visualization
    return response


def onterminate():
    debug('Caught signal... exiting.')
    exit(0)
```


Right away, you notice that there are a whole bunch of decorators (or annotations) and two functions (`dotransform`
and `onterminate`). So what does this all mean and how does it work? Let's focus on the meat, shall we?

The `dotransform` function is the transform's entry point, this is where all the fun stuff happens. This transform
isn't particularly fun, but it serves as a good example of what typically happens in a Sploitego transform.
`dotransform` takes two arguments, `request` and `response`. The `request` object contains the data
passed by Maltego to the local transform and is parsed and stored into the following properties:

* **value**:    a string containing the value of the input entity.
* **fields**:   a dictionary of entity field names and their respective values of the input entity.
* **params**:   a list of any additional command-line arguments to be passed to the transform.

The `response` object is what our data mining logic will populate with entities and it is of type
`MaltegoTransformResponseMessage`. The `response` object is very neat in the sense that it can do magical things
with data. With simple arithematic operations (`+=`, `-=`, `+`, `-`), one can add/remove entities or
Maltego UI messages. You'll probably want to use the `+=` or `-=` operators because `-` and `+` create
a new `MaltegoTransformResponseMessage` and that can be costly. Let's take a look at how it works in the transform
above:

```python
# ...
    e = MypackageEntity('Hello %s!' % request.value)
# ...
    response += e
# ...
```

The first line of code, creates a new `MypackageEntity` object is created with a value 'Hello &lt;request.value&gt;!'.
The second line of code adds the newly created object, `e`, to the `response` object. If we serialize the object
into XML we'd see the following (spaced for clarity):

```xml
<MaltegoMessage>
    <MaltegoTransformResponseMessage>
        <Entities>
            <Entity Type="mypackage.MypackageEntity">
                <Value>Hello Phil!</Value>
                    <Weight>1</Weight>
                    <AdditionalFields>
                        <Field DisplayName="Field 1" MatchingRule="strict" Name="mypackage.field1">2</Field>
                        <Field DisplayName="Field N" MatchingRule="strict" Name="mypackage.fieldN">test</Field>
                    </AdditionalFields>
            </Entity>
        </Entities>
    </MaltegoTransformResponseMessage>
</MaltegoMessage>
```

You may be wondering where those fields (`mypackage.field1` and `mypackage.fieldN`) came from? Simple, from
here:

```python
# ...
    e.field1 = 2
    e.fieldN = 'test'
# ...
```

If your feeling eager, see "4.3.x - Creating a Custom Entity" for more information on how those properties came to
fruition.

Once `dotransform` is called, the data mining logic does it's thing and adds entities to the `response` object
if necessary. Finally, the `response` is returned and `dispatcher` serializes the object into XML. What about
the decorators (`@configure` and `@superuser`)? Read on...


#### 4.3.3 - `sploitego install-package` Magic (`@configure`)

So how does `sploitego install-package` figure out how to install and configure the transform in Maltego's UI? Simple,
just use the `@configure` decorator on your `dotransform` function and `sploitego install` will take care of the rest.
The `@configure` decorator tells `sploitego install-package` how to install the transform in Maltego. It takes the
following named parameters:

* **label**:        the name of the transform as it appears in the Maltego UI transform selection menu
* **description**:  a short description of the transform
* **uuids**:        a list of unique transform IDs, one per input type. The order of this list must match that of the
                    inputs parameter. Make sure you account for entity type inheritance in Maltego. For example, if you
                    choose a `DNSName` entity type as your input type you do not need to specify it again for
                    `MXRecord`, `NSRecord`, etc.
* **inputs**:       a list of tuples where the first item is the name of the transform set the transform should be part
                    of, and the second item is the input entity type.
* **debug**:        Whether or not the debugging window should appear in Maltego's UI when running the transform.

Let's take a look at the code again from the example above:

```python
# ...
@configure(
    label='To MypackageEntity [Hello World]',
    description='Returns a MyPackageEntity entity with the phrase "Hello Word!"',
    uuids=[ 'mypackage.v2.MyPackageEntityToPhrase_HelloWorld' ],
    inputs=[ ( 'Mypackage', Person ) ],
    debug=True
)
def dotransform(request, response):
# ...
```

The example above tells `mtginstall` to process the transform in the following manner:

1. The name of the transform in the transform selection context menu should appear as `To MypackageEntity [Hello World]`
   in Maltego's UI.
2. The short description of the transform as it appears in Maltego's UI is `Returns a MyPackageEntity entity with the
   phrase &quot;Hello Word!&quot;`.
3. The transform ID of the transform in Maltego's UI will be `mypackage.v2.MyPackageEntityToPhrase_HelloWorld`.
   and will only work with an input entity type of `Person` belonging to the `Mypackage` transform set.
4. Finally, Maltego should pop a debug window on transform execution.

What if we wanted this transform to work for entity types of `Location`, as well. Simple, just add another
`uuid` and `input` tuple like so:

```python
# ...
@configure(
    label='To MypackageEntity [Hello World]',
    description='Returns a MyPackageEntity entity with the phrase "Hello Word!"',
    uuids=[ 'mypackage.v2.MyPackageEntityToPhrase_HelloWorld', 'mypackage.v2.MyPackageEntityToLocation_HelloWorld' ],
    inputs=[ ( 'Mypackage', Person ), ( 'Mypackage', Location ) ],
    debug=True
)
def dotransform(request, response):
# ...
```

Now you have one transform configured to run on two different input entity types (`Person` and `Location`) with
just a few lines of code and you can do this as many times as you like! Awesome!


#### 4.3.4 - Running as Root (`@superuser`)

At some point you may want to run your transform using a super-user account in UNIX-based environments. Maybe to run
something cool like Metasploit or Nmap. You can do that simply by decorating `dotransform` with `@superuser`:

```python
# ...
@superuser
@configure(
# ...
)
def dotransform(request, response):
# ...
```

This will instruct `dispatcher` to run the transform using `sudo`. If `dispatcher` is not running as
`root` a `sudo` password dialog box will appear asking the user to enter their password. If successful,
the transform will run as root, just like that!

#### 4.3.5 - Renaming Transforms with `sploitego rename-transform`

Alright, so you got a bit excited and decided to repurpose the `helloworld` transform module to do something cool.
In you're bliss you decided to change the name of the transform module to `mycooltransform.py`. So you're all set to
go, right? **Wrong**, you'll need to change the entry in the `__all__` variable (i.e. `'helloworld'` ->
`'mycooltransform'`) in `src/mypackage/transforms/__init__.py`, first. Why? Because `mtginstall` will only detect
transforms if they are listed in the `__all__` variable of the transform package's `__init__.py` script. You can do this
quite simply by running:

```bash
$ pwd
/home/user1/
$ sploitego rename-transform helloworld mycooltransform
renaming transform 'helloworld' to 'mycooltransform'...
updating __init__.py
done!
```

#### 4.3.6 - Creating More Transforms with `sploitego create-transform`
So you want to create another transform but you want to be speedy like Gonzalez. You don't want to keep writing out the
same thing for each transform. No problem, `sploitego create-transform` will give you a head start. `sploitego create-
transform` generates a bare bones transform module that you can hack up to do whatever you like. Just run `sploitego
create-transform` in the `src/mypackage/transforms` directory, like so:

```bash
$ cd src/mypackage/transforms
$ sploitego create-transform mysecondcooltransform
creating file ./mysecondcooltransform.py...
updating __init__.py
done!
```

No need to add the entry in `__init__.py` anymore because `sploitego create-transform` does it for you automagically.

# Known Issues

## `dispatcher` exit code 1

This issue occurs when the Sploitego scripts are not in the system path of the JVM. To fix this issue you will need to
create symlinks to the Sploitego scripts in one of the directories in your path. Unfortunately, it is not as simple as
adding the directory to your $PATH variable. For some reason JVM determines its PATH in a different way than `bash`,
`csh`, etc. The `fixpath.py` script in the `java` directory was developed to assist in determining what directories in
the JVM's executable path exist. To run it, just do:

```bash
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
```

As seen above, `fixpath.py` compiles `JVMPathChecker.java` and runs it to determine the value of the JVM's PATH
environment variable. From that, it provides you with a list of directory options for which to install the sploitego
scripts to. Once you have selected the appropriate directory, `fixpath.py` will then symlink each of the scripts for you
in the directory of your choice.


