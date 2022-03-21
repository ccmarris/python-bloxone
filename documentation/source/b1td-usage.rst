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
    t.threat_counts().json()
    t.historical_threat_counts().json()
    t.default_ttl().json()
    t.dossier_target_types().json()
    t.dossier_sources().json()
    t.dossier_target_sources().json()
    t.dossierquery("eicar.co").json()
    t.dossierquery([ "eicar.co", "pwn.af" ]).json()
    t.dossierquery([ "eicar.co", "pwn.af" ], sources="atp").json()
    t.dossierquery([ "eicar.co", "pwn.af" ], sources=["atp","whois"]).json()
    t.expand_mitre_vector('DGA').json()
    t.threat_actor('APT1').json()
    # Get Countries and ISO Codes
    t.get_countries().json()
    # Get the ISO Code for a specific country
    t.get_country_isocode(country='Somalia)
    # You can get the IP networks for a country using either the ISO country
    # Code or the Country name e.g.
    t.get_country_ips(country="SO").json()
    t.get_country_ips(country="Somalia").json()
