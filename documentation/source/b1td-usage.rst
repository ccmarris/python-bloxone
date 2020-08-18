==========
b1td Usage
==========

Examples
--------

.. todo::
    These examples are placeholders, useful, but actual example set here is on 
    the todo.

.. code-block:: python

    bloxone.utils.reverse_labels("www.infoblox.com")

    import bloxone
    t = bloxone.b1td('/Users/marrison/configs/emea.ini')
    t.version
    bloxone.__version__

    import bloxone
    tdc = bloxone.b1tdc('/Users/marrison/configs/emea.ini')
    tdc.get('/access_codes').json()
    tdc.get('/cert_download_urls').json()
    tdc.get('/content_categories').json()
    lad = bloxone.b1lad('/Users/marrison/configs/emea.ini')
    lad = bloxone.b1tdlad('/Users/marrison/configs/emea.ini')
    lad.get('/lookalike_domains').json()
    tdc.get('/threat_feeds').json()
    import readline; print('\n'.join([str(readline.get_history_item(i + 1)) for i in range(readline.get_current_history_length())]))
    >>> 
