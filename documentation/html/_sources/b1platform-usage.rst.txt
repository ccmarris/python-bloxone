===================
b1platform Usage
===================

The :class:`b1platform` provides access to unsupported/undocumented plaform 
specific API functions. These should therefore, only be used at the users
own risk. It should also be noted that these could change at any time.



Examples
--------


.. todo::
    These are simple examples to show you usage of the class. More comprehensive
    documentation is on the todo.
    

.. code-block:: python

    from pprint import pprint
    import bloxone

    # Instantiate class with ini file as argument
    platform = bloxone.b1platform('<path to ini>')

    # Get current user details
    repsonse = platform.get_current_user()

    # Get account membership for current user
    response = platform.get_current_user_accounts()

    # Get current tenant name
    name = platform.get_current_tenant()

    # Get list of users
    response = platform.get_users()

    # Retrieve the audit log
    audit_log = platform.auditlog()

    # Audit user accounts (uses domain of current user)
    list_of_non_complient_users = platform.audit_users()

    # Audit user accounts (provide list of domains)
    list = platform.audit_users(domains=['infoblox.com', 'mydomain.com'])
