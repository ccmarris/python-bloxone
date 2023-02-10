===========
b1ntp Usage
===========

The :class:`b1ntp` provides access to generic calls to manage API calls for
NTP management. It inherits the :class:b1platform class so that Additional 
'helper' methods such as get_ophid(), are available.



Examples
--------


.. todo::
    These are simple examples to show you usage of the class. More comprehensive
    documentation is on the todo.
    

.. code-block:: python

    from rich import print
    import bloxone

    # Instantiate class with ini file as argument
    b1n = bloxone.b1ntp('<path to ini>')

    repsonse = b1n.get('/account/config')

    # Get config for specific OPH
    ophid = b1n.get_ophid('MyOPH')
    objpath = f'/host/config/{ophid}'
    response = b1n.get(objpath)

    # Get Status
    objpath = f'/status/config/{ophid}'
    response = b1n.get(objpath)