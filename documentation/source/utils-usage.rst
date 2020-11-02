====================
Additional Utilities
====================

The :mod:`utils` sub-module contains a set of data Utilities for data validation
and normalisation. Typically used for IoCs when using the :mod:`bloxone.b1td`
methods for searches against TIDE. 

For performance purposes when handling bulk data, the :func:`data_type()`,
:func:`validate_fqdn()` and :func:`validata_url()` functions use pre-compliled
regexes that are created using the :func:`buildregex()` function, that returns
host and url regexes as a tuple.

These can then be passed to the appropriate data function.

For example::

    import bloxone
    host_regex, url_regex = bloxone.utils.buildregex()
    qdata = "my.host.name.com"
    data_type = bloxone.utils.data_type(qdata, host_regex, url_regex)
    # Result = 'host'
    qdata = "http://my.host.name.com"
    data_type = bloxone.utils.data_type(qdata, host_regex, url_regex)
    # Result = 'url'


