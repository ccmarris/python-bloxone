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
    bloxone.__version__
    t = bloxone.b1td('/Users/marrison/configs/emea.ini')
    t.tide_url
    t.threat_classes().json()
    t.threat_properties().json()
    t.threat_properties(threatclass="malwareC2").json()
    t.threat_properties(threatclass="malwareC2").json()
    t.dossierquery("eicar.co").json()
    t.expand_mitre_vector('DGA').json()
    t.threat_actor('APT1').json()
