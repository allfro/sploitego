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

    $ sploitego create-package mypackage
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


Creating and Removing Transforms
--------------------------------

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
automagically. The same is true for ``sploitego delete-transform`` if you want to remove a transform from your package.


.. _custom-entity:

Creating Custom Entities
========================

Now you want to get a custom entity in. No problem! We've got that covered too. With just a few lines of code you can
create as many entities as you wish. The only gotcha in this process is that you'll probably want to iconify these
entities so they look good in Maltego. That's a manual process we can't get away from. On the other hand, defining
custom entities in your code is quite simple. Take a look inside your custom package's
``src/mypackage/transforms/common/entities.py`` file. It should look similar to this:

.. code-block:: python

    #!/usr/bin/env python

    from sploitego.maltego.message import Entity, EntityField, EntityFieldType, MatchingRule

    # ...

    """
    DO NOT EDIT
    ...
    """
    class FooEntity(Entity):
        namespace = 'foo'


    """
    TODO
    ...
    """
    @EntityField(name='foo.fieldN', propname='fieldN', displayname='Field N', matchingrule=MatchingRule.Loose)
    @EntityField(name='foo.field1', propname='field1', displayname='Field 1', type=EntityFieldType.Integer)
    class MyFooEntity(FooEntity):
        # ...
        # name = my.fancy.EntityType
        pass

You may be asking yourself "That's it?" or maybe even scratching your head about what this all means. Don't worry, we'll
go through this line-by-line. The first class, :py:class:`FooEntity` is the base entity class for all your custom
entities. You won't want to edit this much since all it provides is a custom namespace for your entities. What is a
namespace? If you've designed a custom entity in Maltego you probably noticed that the entity gets a suggested ID of
``<username>.<EntityName>``. In this case the namespace is the ``<username>`` portion of the entity's ID. This is done
to avoid conflicts between different entity definitions from various transform developers. Maltego's built-in entities
have a namespace of ``maltego``. In our case, the namespace for all of our entities will be ``foo``.

What about the other entity, :py:class:`MyFooEntity`? That's just an example entity definition that you can modify to
your heart's content. Notice the :py:func:`@EntityField` decorators. Those define the structure of the entity in terms
of what entity fields exist, their data-types, icon decorators, and various other elements that affect how Maltego
compares two different entities of the same type. In addition, these decorators synthesize class fields identified by
the ``propname`` keyword argument. Modifying their values is as easy as ``myfooentity.mypropname``.

You can specify as many entity fields as you want by just adding an extra :py:func:`@EntityField` decorator to your
entities. The :py:func:`@EntityField` decorator takes the following parameters:

.. py:function:: @EntityField(**kwargs)

    :keyword str name: the name of the field without spaces or special characters except for dots ('.') (required).
    :keyword str propname: the name of the object's property used to get and set the value of the field
                           (required, if name contains dots)
    :keyword str displayname: the name of the entity as it appears in Maltego (optional).
    :keyword str type: the data type of the field (optional, default: EntityFieldType.String).
    :keyword bool required: whether or not the field's value must be set before sending back the message (optional,
                            default: False).
    :keyword list choices: a list of acceptable field values for this field (optional).
    :keyword str matchingrule: whether or not the field should be loosely or strictly matched by Maltego's graphing
                               engine (optional, default: MatchingRule.Strict).
    :keyword callable decorator: a function that is invoked each and every time the field's value is set or changed.


Matching Rules
--------------

Maltego currently supports two types of matching rules for entities: ``strict`` and ``loose``. These rules apply to an
entity's fields and determine how Maltego graph two entities of the same type and value but with differing entity field
values on a graph. For example, let's assume you've performed a transform that produced two ``IPv4Address`` entities on
a graph with the same entity value of ``127.0.0.1``. Each ``IPv4Address`` entity has an ``internal`` boolean field
which indicates whether or not the ``IPv4Address`` entity represents an internal IP address. Let's assume that the
``internal`` fields are different, one is set to ``true`` and the other to ``false``. In the case where the ``internal``
field is ``loose``'ly matched, both entities would appear as one entity on the graph. Otherwise, if the ``internal``
field is ``strict``'ly matched, then both these entities would appear as two separate entities on the graph. If you're a
fan of a visual example, try the following example transform out to see what the end results are:

.. code-block:: python

    #!/usr/bin/env python

    from sploitego.maltego.message import Entity, MatchingRule
    from sploitego.maltego.message import Phrase, Field
    from sploitego.framework import configure


    class TestEntity(Entity):
        namespace='test'

    class MyIPv4Address(TestEntity):
        pass


    @configure(
        label='To IPv4Address [Matching Rules]',
        description='Shows how matching rules work in Maltego.',
        uuids=[ 'tests.v2.PhraseToIPv4Address_Matching_Rules' ],
        inputs=[ ( 'Testing Matching Rules', Phrase ) ],
        debug=True
    )
    def dotransform(request, response):

        # What kind of matching rule are we using?
        mr = MatchingRule.Strict
        if request.value.lower() == 'loose':
            mr = MatchingRule.Loose

        # First IP
        ip1 = MyIPv4Address('127.0.0.1')
        ip1 += Field('internal', 'true', matchingrule=mr)
        response += ip1

        # Second IP
        ip2 = MyIPv4Address('127.0.0.1')
        ip2 += Field('internal', 'false', matchingrule=mr)
        response += ip2

        # Return response for visualization
        return response


The example transform runs on ``Phrase`` entities and determines its matching rule based on the ``Phrase`` entity's
value. If it is anything other than ``loose``, the entity field ``internal`` will be ``strict``'ly matched.

Entity Field Decorators
-----------------------

Say you want to provide users of your transforms with better visuals for your transform outputs. For example,