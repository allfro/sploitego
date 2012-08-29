#!/usr/bin/env python

from sys import platform

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = ['Nadeem Douba']

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


if platform == 'darwin':
    from subprocess import Popen
    from Tkinter import Tk
    Tk().destroy()
    Popen(['osascript', '-e', 'tell application "Python" to activate'])