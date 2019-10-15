# !/usr/bin/env python

import sys
import os

sys.path.insert(0, 'src')

import sploitego

from setuptools import setup, find_packages, os

scripts = [
    'src/scripts/qtmsfconsole'
]

if os.name == 'nt':
    scripts += ['%s.bat' % s for s in scripts]

setup(
    name='sploitego',
    author='Nadeem Douba',
    version=sploitego.__version__,
    author_email='ndouba@gmail.com',
    description='Penetration testing transforms for Maltego.',
    license='GPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    scripts=scripts,
    zip_safe=False,
    package_data={
        '': ['*.gif', '*.png', '*.conf', '*.mtz', '*.machine']
    },
    install_requires=[
        'scapy==2.4.1',
        'pynessusrpc',
        'pyiptools',
        'pymetasploit',
        'canari',
        'dnspython',
        'lxml'
    ],
    dependency_links=[
        'http://www.secdev.org/projects/scapy/files/'
    ]
)

try:
    print 'Detecting PySide installation...'
    import PySide
    print 'PySide is installed, no further action required.'
except ImportError:
    print 'PySide not detected. Opening browser to PySide download page ' \
          '(http://qt-project.org/wiki/Category:LanguageBindings::PySide::Downloads)'
    import webbrowser
    webbrowser.open_new('http://qt-project.org/wiki/Category:LanguageBindings::PySide::Downloads')

print "Please install and configure metasploit and postgresql (for msf db) if you haven't done so already."