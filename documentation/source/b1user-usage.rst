=============
b1user Usage
=============

Examples
--------

.. todo::
    These are simple examples to show basic syntax.

.. code-block:: python

    import bloxone
    b1u = bloxone.b1user(username='myuser', email_domain='myzone.com', 
                         b1org='My Tenant Name', cfg_file='bloxone.ini')
    b1u.owner
    b1u.email_domain
    b1u.user_exists()
    b1u.find_user_objects()
    b1u.data_report()
    b1u.is_current_user()
    b1u.current_org
    b1u.check_tenant()
