===========
b1oph Usage
===========

The :class:`b1oph` provides generic calls to manage API calls for OPH 
management. Additional 'helper' methods such as get_ophid().

.. todo::
    Service status
    Service management
    Rename OPH

Examples
--------


.. todo::
    These are simple examples to show you usage of the class. More comprehensive
    documentation is on the todo.
    

.. code-block:: python

    from pprint import pprint
    import bloxone

    # Instantiate class with ini file as argument
    oph = bloxone.b1oph('<path to ini>')

    # Get the ophid 
    ophid = b1oph.get_ophid(name='youroph-name')


