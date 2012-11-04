Sploitego - Maltego's (Local) Partner in Crime
==============================================

## 1.0 - Introduction

Sploitego is a local pen-test transform package that uses the [Canari Framework](https://github.com/allfro/canari) for
local transform execution in [Maltego](http://paterva.com/). The framework was first introduced at DEFCON 20 and has
since picked up steam.

## 2.0 - Installing Sploitego

### 2.1 - Supported Platforms
Sploitego has currently been tested on Mac OS X and Linux.

### 2.2 - Requirements
Sploitego is only supported on Python version 2.6. The setup script will automatically download and install most of the
prerequisite modules, however, some modules will still need to be installed manually. The following modules require
manual installation:
* **Scapy 2.1.0**: See the
  [Scapy Installation Manual](http://www.secdev.org/projects/scapy/doc/installation.html) for build
  instructions pertaining to your operating system.

Some of the transforms require external command-line tools (e.g. nmap, amap, p0f, etc.). The following command-line
tools are currently supported:
* **Nmap version 5.51**: [Download](http://nmap.org/dist/?C=M&O=D)
* **P0f version 3.05b**: [Download](http://lcamtuf.coredump.cx/p0f3/releases/p0f-3.05b.tgz)
* **Amap version 5.4**: [Download](http://www.thc.org/releases/amap-5.4.tar.gz)
* **Metasploit**: [Download](http://downloads.metasploit.com/data/releases/framework-latest.tar.bz2)
* **Nessus**: [Download](http://www.tenable.com/products/nessus/nessus-product-overview)

### 2.3 - Installation
Once you've installed the necessary prerequisites, installing Sploitego is a cinch. Just run:

```bash
$ sudo python setup.py install
```

This will install all the necessary modules and download any dependencies (other than what's required above)
automatically. Once Sploitego has been installed, it's time to install the transforms. First, make sure Maltego has been
run for the first time and initialized (i.e. logged in, transforms discovered, etc.). Once initialized, shutdown Maltego
and run the following command:

```bash
$ canari install-package sploitego
```


# Contact Info

Right now we only have one contributor:

- Nadeem Douba: @ndouba on Twitter

Contact us any time! Sploitego is currently looking for help in various areas of the project.
