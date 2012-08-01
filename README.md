Sploitego - Maltego's (Local) Partner in Crime
==================================================

## 1.0 - Introduction

Sploitego is a **rapid** local transform development framework for [Maltego][1] written in Python. Sploitego's core
features include:

- An easily **extensible and configurable** framework;
- A set of **powerful** and **easy-to-use** scripts for debugging, configuring, and installing transforms;
- A **plethora** of auxiliary modules focused on [Open Source Intelligence (OSINT)][2] gathering as well as
  **penetration testing**;
- Finally, a great number of **really awesome pen-testing transforms**.

The original focus of Sploitego was to provide a set of transforms that would aid in the execution of penetration tests,
and vulnerability assessments. Ever since it's first prototype, it has become evident that the framework can be used for
much more than that. Sploitego is perfect for anyone wishing to graphically represent their data in [Maltego][1] without
the hassle of learning a whole bunch of unnecessary stuff. It has generated interest from digital forensics analysts to
pen-testers, and even [psychologists][3].

## 2.0 - Why Use Sploitego?

### 2.1 - Extensibility
To develop *local* transforms for Maltego with *ease*; no need to learn XML, the local transform [specification][3], or
develop tedious routines for command-line input parsing, debugging, or XML messaging. All you need to do is focus on
developing the core data mining logic and Sploitego does the rest. Sploitego's interface is designed on the principles
of [convention over configuration][5] and [KISS][6].

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
* **libdnet:** [Download][7] (See the [Scapy Installation Manual for more details][8])
* **sip & PyQt4**: [Download][9]

Some of the transforms require external command-line tools (e.g. nmap, amap, p0f, etc.). The following command-line
tools are currently supported:
* **Nmap version 5.51**: [Download][10]
* **P0f version 3.05b**: [Download][11]
* **Amap version 5.4**: [Download][12]
* **Metasploit**: [Download][13]
* **Nessus**: [Download][14]

### 3.3 - Installation
Once you've installed the necessary prerequisites, installing Sploitego is a cinch. Just run:

```bash
$ sudo python setup.py install
```

This will install all the necessary modules and download any dependencies (other than libdnet and PyQt4) automatically.
Once Sploitego has been installed, it's time to install the transforms. First, make sure Maltego is not running and run:

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
If you're unsure, pick your home directory (e.g. ```~/```). If successful, you will see the following output in your
terminal:

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




[1]: http://paterva.com/
[2]: http://en.wikipedia.org/wiki/Open-source_intelligence
[3]: http://www.forbes.com/sites/kashmirhill/2012/07/20/using-twitter-to-help-expose-psychopaths
[4]: http://paterva.com/web5/documentation/localtransforms.php
[5]: http://en.wikipedia.org/wiki/Convention_over_configuration
[6]: http://en.wikipedia.org/wiki/KISS_principle
[7]: http://libdnet.googlecode.com/files/libdnet-1.12.tgz
[8]: http://www.secdev.org/projects/scapy/doc/installation.html#install-from-original-sources
[9]: http://www.riverbankcomputing.co.uk/software/pyqt/download/
[10]: http://nmap.org/dist/?C=M&O=D
[11]: http://lcamtuf.coredump.cx/p0f3/releases/p0f-3.05b.tgz
[12]: http://www.thc.org/releases/amap-5.4.tar.gz
[13]: http://downloads.metasploit.com/data/releases/framework-latest.tar.bz2
[14]: http://www.tenable.com/products/nessus/nessus-product-overview