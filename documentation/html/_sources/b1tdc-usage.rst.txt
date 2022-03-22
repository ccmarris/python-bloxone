===========
b1tdc Usage
===========

Examples
--------

.. todo::
    These examples are placeholders, useful, but actual example set here is on 
    the todo.

.. code-block:: python

    import bloxone
    tdc = bloxone.b1tdc('/Users/marrison/configs/emea.ini')
    tdc.get('/access_codes').json()
    tdc.get('/cert_download_urls').json()
    tdc.get('/content_categories').json()
    tdc.get('/threat_feeds').json()
    # Custom list methods
    tdc.get_custom_lists().json()
    tdc.get_custom_list(name='listname').json()
    tdc.create_custom_list(name='mylist', 
                           confidence='HIGH', 
                           items=['facebook.com', 'instagram.com'])
    tdc.delete_custom_list(name=['mylist','mylist2'])
