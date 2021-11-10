==================
Usage and Examples
==================

Inifile configuration
---------------------

A sample inifile for the bloxone module is shared as *bloxone.ini* and follows
the following format provided below::

    [BloxOne]
    url = 'https://csp.infoblox.com'
    api_version = 'v1'
    api_key = '<you API Key here>'

You can therefore simply add your API Key, and this is ready for the bloxone
module used by the automation demo script. Legacy, interactive and service API
keys are supported.


Overview
--------

The aim of this module is to provide simple object based access to the 
BloxOne APIs and make it as simple as possible to code given the available
swagger documentation. 

There are several classes/subclasses that provide this access. The base
class is :class:`b1`. This acts as a parent class for the BloxOne Application
APIs.

The specific API 'trees' are then split in to subclasses of :class:`b1`:

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

    :class:`b1anycast` 
        Access to the BloxOne Anycast API with a generic
        *get*, *create*, *delete* and *update* methods plus specific task 

    :class:`b1authn` 
        Access to the BloxOne On-Prem Authentication Service API with generic
        *get*, *create*, *delete* and *update* methods plus specific task 

    :class:`b1bootstrap` 
        Access to the BloxOne On-Prem Bootstrap App API with generic
        *get*, *create*, *delete* and *update* methods plus specific task 

    :class:`b1cdc` 
        Access to the BloxOne Data Connector API with generic
        *get*, *create*, *delete* and *update* methods plus specific task 

    :class:`b1diagnostics` 
        Allows the user to execute remote commands on an OPH via the API

    :class:`b1oph` 
        Access to the BloxOne On Prem Host API with generic
        *get*, *create*, *delete* and *update* methods plus specific tasks
        to allow simple status reporting, App control, etc. 

    :class:`b1platform` 
        Methods to provide access to users and audit log information

    :class:`b1sw` 
        Access to the BloxOne Software Upgrade Scheduling API with generic
        *get*, *create*, *delete* and *update* methods plus specific task 

    :class:`b1ztp` 
        Access to the BloxOne On Prem Host Host Activation API with generic
        *get*, *create*, *delete* and *update* methods plus specific task 

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


Generic API Wrapper
-------------------

It is also possible to use the bloxone.b1 class as a generic API wrapper with public methods
for *get*, *create*, *update* and *delete*. These can be used to pass a full URL, and where 
appropriate body and parameters. It is of course possible to build the URL using the attributes
of this class, in addition to manually entering the full url::

    import bloxone
    b1 = bloxone.b1(<ini file>)
    url = 'https://csp.infoblox.com/api/ddi/v1/ipam/ip_space'
    response = b1.get(url)
    print(response.json())

    url = b1.ddi_url + '/ipam/ip_space'
    response = b1.get(url, _filter='name=="test_ip_space"')
    print(response.json())


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
    b1diagnostics-usage
    b1td-usage
    b1tdc-usage
    b1tdep-usage
    b1tddfp-usage
    b1tdlad-usage
    b1oph-usage
    b1platform-usage
    utils-usage

The remaining classes generally provide generic interfaces for *get*, *create*, *update* and *delete*.
Usage follows the same format of instantiating the class with an ini file and accessing the generic methods
using using the 'swagger' path for the appropriate object.

