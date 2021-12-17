===========
b1oph Usage
===========

The :class:`b1oph` provides generic calls to manage API calls for OPH 
management. Additional 'helper' methods such as get_ophid(), and the 
ability to see the status of OPHs, Apps, and provide App control.

.. todo::
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


    # Get status for all OPHs
    >>> pprint.pprint(b1oph.oph_status_summary())
    # Get status for specific OPH
    >>> pprint.pprint(b1oph.oph_status_summary(name="my-oph-name"))
    {'my-oph-name': {'applications': {'Anycast': 'disabled - stopped',
                                        'CDC': 'disabled - stopped',
                                        'CDC_version': 'v2.1.3',
                                        'DFP': 'disabled - stopped',
                                        'DFP_version': 'v2.1.5',
                                        'DHCP': 'active',
                                        'DHCP_version': 'v3.1.8',
                                        'DNS': 'active',
                                        'DNS_version': 'v3.1.4',
                                        'NGC': 'disabled - stopped'},
                        'host_type': 'BloxOne Appliance - B105',
                        'id': '97310',
                        'ip_address': '192.168.1.102',
                        'last_seen': '2021-11-04T19:46:55.942540Z',
                        'nat_ip': None,
                        'status': {'Application Management': 'Online',
                                    'OPH State': 'Online',
                                    'Platform Management': 'Online'},
                        'version': 'v4.3.6'}}

    # Get status for individual app on specified OPH
    >>> b1oph.get_app_state(name="my-oph-name", app="DNS")
    'active'
    # Get status for individual app on specified OPH
    >>> b1oph.get_app_state(name="my-oph-name", app="CDC")
    'disabled - stopped'

    # Perform an action on a an App for specified OPH
    >>> b1oph.manage_app(name="my-oph-name", app="CDC", action="start")
    False
    >>> b1oph.manage_app(name="my-oph-name", app="CDC", action="enable")
    True
    >>> b1oph.get_app_state(name="non-existent-oph", app="DNS")
    ERROR:root:OPH: non-existant-oph not found
    'OPH: non-existent-oph not found'

    # Specific methods can also be directly called
    >>> b1oph.get_app_state(name="my-oph-name", app="CDC")
    'stopped'
    >>> b1oph.get_app_state(name="my-oph-name", app="CDC")
    'stopped'
    >>> b1oph.manage_app(name="my-oph-name", app="CDC", action="disable")
    True
    >>> b1oph.get_app_state(name="my-oph-name", app="CDC")
    'disabled - stopped'
    >>> b1oph.enable_app(name="my-oph-name", app="CDC")
    True
    >>> b1oph.disable_app(name="my-oph-name", app="CDC")
    True
    
    >>> b1oph.manage_app(name="my-oph-name", app="CDC", action="blah")
    ERROR:root:Action: blah not supported
    False