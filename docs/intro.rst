############
Introduction
############

Sploitego is a **rapid** local transform development framework for `Maltego <http://paterva.com/>`_ written in Python.
The original focus of Sploitego was to provide a set of transforms that would aid in the execution of penetration tests,
and vulnerability assessments. Ever since it's first prototype, it has become evident that the framework can be used for
much more than that. Sploitego is perfect for anyone wishing to graphically represent their data in
`Maltego <http://paterva.com>`_ without the hassle of learning a whole bunch of unnecessary stuff. It has generated
interest from digital forensics analysts to pen-testers, and even
`psychologists <http://www.forbes.com/sites/kashmirhill/2012/07/20/using-twitter-to-help-expose-psychopaths>`_.
Sploitego's core features include:

* An easily **extensible and configurable** framework that promotes **maximum reusability**;
* A set of **powerful** and **easy-to-use** scripts for debugging, configuring, and installing transforms;
* A **plethora** of auxiliary modules focused on
  `Open Source Intelligence (OSINT) <http://en.wikipedia.org/wiki/Open-source_intelligence>`_ gathering as well as
  **penetration testing**;
* Finally, a great number of **really awesome pen-testing transforms**.

Terminology
===========

Before we get started with the documentation, it might be useful to introduce some of the terminology that will be used
throughout the documentation:

* **Entity**: a piece of information on a Maltego graph represented as a node.
* **Transform**: a function that takes one entity as input and produces zero or more entities as output.
* **Input Entity**: the entity that is being passed into the transform to use for data mining purposes.
* **Output Entity**: the entity that is being returned by the transform to be drawn on a Maltego graph.
* **Transform Module**: a python module local transform code.
* **Transform Package**: a python package containing one or more transform modules.

Why Use Sploitego?
==================

To develop *local* transforms for Maltego with *ease*; no need to learn XML, the local transform
`specification <http://paterva.com/web5/documentation/localtransforms.php>`_, or develop tedious routines for command-
line input parsing, debugging, or XML messaging. All you need to do is focus on developing the core data mining logic
and Sploitego does the rest. Sploitego's interface is designed on the principles of
`convention over configuration <http://en.wikipedia.org/wiki/Convention_over_configuration>`_ and
`KISS <http://en.wikipedia.org/wiki/KISS_principle>`_.

For example, this is what a local transform looks like using Sploitego:

.. code-block:: python

    #!/usr/bin/env python

    from sploitego.maltego.message import Phrase

    def dotransform(request, response):
        response += Phrase('Hello %s' % request.value)
        return response


And this is what a custom-defined entity looks like:

.. code-block:: python

    class MyEntity(Entity):
        pass


If you're already excited about using Sploitego, wait until you see the other features it has to offer!