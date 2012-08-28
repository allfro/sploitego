################################
Transform Development Quickstart
################################

The following sections will give you a quick-start tutorial on how to develop transforms.

Creating a Transform Package
============================

Developing transforms is now easier than ever. If you want to create a whole bunch of transforms or if you wish to take
advantage of ``sploitego install-package`` then you'll want to create a transform package. Otherwise, you'll have to
manually install and configure your local transform in the Maltego UI (ouch!). We'll just go ahead and create a
transform package called :py:mod:`mypackage` because I have a good feeling you'll be really eager to create a whole
bunch of transforms::

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


You'll notice that a simple skeleton project was generated, with a :py:mod:`helloworld` transform to get you started.
You can test the :py:mod:`helloworld` transform module right away by running `sploitego debug-transform` like so::


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


Developing a Transform
======================

Let's take a look at an abbreviated version of  ``src/mypackage/transforms/helloworld.py``, from our example above,
to see how this transform was put together:

.. code-block:: python

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


Right away, you notice that there are a whole bunch of decorators (or annotations) and two functions
(:py:func:`dotransform` and :py:func:`onterminate`). So what does this all mean and how does it work? Let's focus on the
meat, shall we?

The :py:func:`dotransform` function is the transform's entry point, this is where all the fun stuff happens. This
transform isn't particularly fun, but it serves as a good example of what typically happens in a Sploitego transform.
:py:func:`dotransform` takes two arguments, :py:obj:`request` and :py:obj:`response`. The :py:obj:`request` object
contains the data passed by Maltego to the local transform and is parsed and stored into the following properties:

.. py:attribute:: value

    A string containing the value of the input entity.

.. py:attribute:: fields

    A dictionary of entity field names and their respective values of the input entity.

.. py:attribute:: params

    A list of any additional command-line arguments to be passed to the transform.

The :py:obj:`response` object is what our data mining logic will populate with entities and it is of type
:py:class:`MaltegoTransformResponseMessage`. The :py:obj:`response` object is very neat in the sense that it can do
magical things with data. With simple arithematic operations (``+=``, ``-=``, ``+``, ``-``), one can add/remove entities
or Maltego UI messages. You'll probably want to use the ``+=`` or ``-=`` operators because ``-`` and ``+`` create
a new :py:class:`MaltegoTransformResponseMessage` object and that can be costly. Let's take a look at how it works in
the transform above:

.. code-block:: python

    # ...
        e = MypackageEntity('Hello %s!' % request.value)
    # ...
        response += e
    # ...


The first line of code, creates a new :py:class:`MypackageEntity` object is created with a value
``'Hello <request.value>!'``. The second line of code adds the newly created object, :py:data:`e`, to the
:py:obj:`response` object. If we serialize the object into XML we'd see the following (spaced for clarity) output:

.. code-block:: xml

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


You may be wondering where those fields (``mypackage.field1`` and ``mypackage.fieldN``) came from? Simple, from here:

.. code-block:: python

    # ...
        e.field1 = 2
        e.fieldN = 'test'
    # ...


If your feeling eager, see :ref:`custom-entity` for more information on how those properties came to fruition.

Once :py:func:`dotransform` is called, the data mining logic does it's thing and adds entities to the
:py:obj:`response` object if necessary. Finally, the :py:obj:`response` is returned and :program:`dispatcher`
serializes the object into XML. What about the decorators (:py:func:`@configure` and :py:func:`@superuser`)?
Read on...


``sploitego install-package`` Magic (:py:func:`@configure`)
-----------------------------------------------------------

So how does ``sploitego install-package`` figure out how to install and configure the transform in Maltego's UI? Simple,
just use the :py:func:`@configure` decorator on your :py:func:`dotransform` function and ``sploitego install`` will take
care of the rest. The :py:func:`@configure` decorator tells ``sploitego install-package`` how to install the transform
in Maltego. It takes the following named parameters:

.. py:function:: @configure(**kwargs)

    :keyword str label: The name of the transform as it appears in the Maltego UI transform selection menu.
    :keyword str description: A short description of the transform.
    :keyword list uuids: A list of unique transform IDs, one per input type. The order of this list must match that of
                        the inputs parameter. Make sure you account for entity type inheritance in Maltego. For example,
                        if you choose a :py:class:`DNSName` entity type as your input type you do not need to specify it
                        again for :py:class:`MXRecord`, :py:class:`NSRecord`, etc.
    :keyword list inputs**: A list of tuples where the first item is the name of the transform set the transform should
                            be part of, and the second item is the input entity type.
    :keyword bool debug: Whether or not the debugging window should appear in Maltego's UI when running the transform.

Let's take a look at the code again from the example above:

.. code-block:: python

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


The example above tells ``sploitego install-package`` to process the transform in the following manner:

#. The name of the transform in the transform selection context menu should appear as
   ``To MypackageEntity [Hello World]`` in Maltego's UI.
#. The short description of the transform as it appears in Maltego's UI is ``Returns a MyPackageEntity entity with the
   phrase "Hello Word!"``.
#. The transform ID of the transform in Maltego's UI will be ``mypackage.v2.MyPackageEntityToPhrase_HelloWorld``. and
   will only work with an input entity type of :py:class:`Person` belonging to the ``Mypackage`` transform set.
#. Finally, Maltego should pop a debug window on transform execution.

What if we wanted this transform to work for entity types of :py:class:`Location`, as well. Simple, just add another
``uuid`` and ``input`` tuple like so:

.. code-block:: python

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


Now you have one transform configured to run on two different input entity types (:py:class:`Person` and
:py:class:`Location`) with just a few lines of code and you can do this as many times as you like! Awesome!


Running as Root (:py:func:`@superuser`)
---------------------------------------

At some point you may want to run your transform using a super-user account in UNIX-based environments. Maybe to run
something cool like :program:`Metasploit` or :program:`Nmap`. You can do that simply by decorating
:py:func:`dotransform` with :py:func:`@superuser`:

.. code-block:: python

    # ...
    @superuser
    @configure(
    # ...
    )
    def dotransform(request, response):
    # ...


This will instruct :program:`dispatcher` to run the transform using :program:`sudo`. If :program:`dispatcher` is not
running as ``root`` a :program:`sudo` password dialog box will appear asking the user to enter their password.
If successful, the transform will run as root, just like that!

Renaming Transforms with ``sploitego rename-transform``
-------------------------------------------------------

Alright, so you got a bit excited and decided to re-purpose the :py:mod:`helloworld` transform module to do something
cool. In you're bliss you decided to change the name of the transform module to ``mycooltransform.py``. So you're all
set to go, right? **Wrong**, you'll need to change the entry in the :py:data:`__all__` variable (i.e. ``'helloworld'``
-> ``'mycooltransform'``) in ``src/mypackage/transforms/__init__.py``, first. Why? Because ``sploitego install-package``
will only detect transforms if they are listed in the :py:data:`__all__` variable of the transform package's
``__init__.py`` script. You can do this quite simply by running::

    $ pwd
    /home/user1/foo/src/foo/transforms
    $ sploitego rename-transform helloworld mycooltransform
    renaming transform 'helloworld' to 'mycooltransform'...
    updating __init__.py
    done!


Creating More Transforms with ``sploitego create-transform``
------------------------------------------------------------

So you want to create another transform but you want to be speedy like Gonzalez. You don't want to keep writing out the
same thing for each transform. No problem, ``sploitego create-transform`` will give you a head start.
``sploitego create-transform`` generates a bare bones transform module that you can hack up to do whatever you like.
Just run ``sploitego create-transform`` in the ``src/mypackage/transforms`` directory, like so::

    $ cd src/mypackage/transforms
    $ sploitego create-transform mysecondcooltransform
    creating file ./mysecondcooltransform.py...
    updating __init__.py
    done!


No need to add the entry in ``__init__.py`` anymore because ``sploitego create-transform`` does it for you
automagically.


.. _custom-entity:

Creating a Custom Entity
------------------------

TODO

.. _known-issues:

Known Issues
============

:program:`dispatcher` exit code 1
---------------------------------

This issue occurs when the Sploitego scripts are not in the system path of the JVM. To fix this issue you will need to
create symlinks to the Sploitego scripts in one of the directories in your path. Unfortunately, it is not as simple as
adding the directory to your ``$PATH`` variable. For some reason JVM determines its PATH in a different way than
``bash``, ``csh``, etc. The :program:`fixpath.py` script in the ``java`` directory was developed to assist in
determining what directories in the JVM's executable path exist. To run it, just do::

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


As seen above, :program:`fixpath.py` compiles ``JVMPathChecker.java`` and runs it to determine the value of the JVM's
PATH environment variable. From that, it provides you with a list of directory options for which to install the
sploitego scripts to. Once you have selected the appropriate directory, :program:`fixpath.py` will then symlink each of
the scripts for you in the directory of your choice.