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
    t.tide_url
    t.threat_classes().json()
    t.threat_properties().json()
    t.threat_properties(threatclass="malwareC2").json()
    t.threat_properties(threatclass="malwareC2").:wjson()
