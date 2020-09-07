==================
Usage and Examples
==================

The aim of this module is to provide simple object based access to the 
BloxOne APIs and make it as simple as possible to code given the available
swagger documentation. 

There are several classes/subclasses that provide this access. The base
class is :class:`b1`. This acts as a parent class for the BloxOne Application
APIs.

The specific API 'trees' are then split in to subclasses of :class:`b1`:

    :class:`b1platform` 
        Providing access to API calls associated with the BloxOne platform
        itself.

    :class:`b1ddi` 
        Access to the BloxOne DDI API with core methods for *get*, *create*,
        *delete* and *update* in addition to specific task orientated helper
        methods.

    :class:`b1td` 
        Access to the Infoblox TIDE API with a generic *get* method plus 
        specific task orientated helper methods.

    :class:`b1tdc` 
        Access to the BloxOne Threat Defence Cloud API with a generic
        *get*, *create*, *delete* methods plus specific task orientated 
        helper methods.

    :class:`b1tdep` 
        Access to the BloxOne Threat Defence Cloud API with a generic
        *get*, *create*, *delete* and *update* methods plus specific task 
        orientated helper methods.

    :class:`b1tddfp` 
        Access to the BloxOne Threat Defence Cloud API with a generic
        *get*, and *update* methods plus specific task orientated helper 
        methods.

    :class:`b1tdlad` 
        Access to the BloxOne Threat Defence Cloud API with a generic
        *get*, method. 


In addition to the API interfaces a set of data handling functions is provided
in the :mod:`utils` sub-module.

Basic Usage
-----------

Using BloxOne DDI as an example, the basic usage structure for a *get* is::

    import bloxone
    b1ddi = bloxone.b1ddi(<ini file>)
    response = b1ddi.get(<object path>)
    if response.status_code in b1ddi.return_codes_ok:
        print(response.text)
    else: 
        print(response.status_code)

Similarly for the other core functions, and classes. For details on method
specific parameters, please see the :doc:`class documentation </classes>`

For debugging purposes, the :mod:`bloxone` module supports logging using 
:mod:`logging` using DEBUG.

.. warning::

    I have attempted to keep debugging clean, however, there is still potential
    for the debug output to produce full data dumps of API responses.


Examples
--------

Although the basic flow of: instantiating the class with a configuration ini 
file; access the attributes or methods, with *get* almost being universal
as a method, and using the swagger object paths to access the required 
resource. Specific examples for each of the classes, and their use, is shown 
in more detail in the following documents, as well as the usage of :mod:`utils`:

.. toctree::
    :maxdepth: 4

    b1ddi-usage
    b1td-usage
    b1tdc-usage
    b1tdep-usage
    b1tddfp-usage
    b1tdlad-usage
    utils-usage
