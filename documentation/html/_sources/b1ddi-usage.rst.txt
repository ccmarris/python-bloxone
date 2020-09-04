=========================
Examples for class: b1ddi
=========================

The aim of this class is to provide simple object based access to the 
BloxOne DDI API and make it as simple as possible to code given the available
swagger documentation. 


Basic Usage
-----------

For BloxOne DDI therefore the basic usage structure for a *get* is::

    import bloxone
    b1ddi = bloxone.b1ddi(<cini file>)
    response = b1ddi.get(<object path>)
    if response.status_code in b1ddi.return_codes_ok:
        print(response.text)
    else: 
        print(response.status_code)

With create and update the key difference is that a JSON body is supplied::

    payload = '{ "address": "10.0.0.0", "cidr": "24" }'
    response = b1ddi.create('/ipam/subnet', body=payload)
    if repsonse.status_code in b1ddi.return_codes_ok:
        print(repsonse.text)
    else: 
        print(response.status_code)
        print(response.text)

For a complete list of supported methods and details around parameters, 
please see the :doc:`class documentation </classes>`


Examples
--------

.. todo::
    These examples are placeholders, useful, but actual example set here is on 
    the todo.

.. code-block:: python

    # Note this is a set of rough examples to show method calls

    import bloxone
    import logging

    log=logging.getLogger(__name__)
    # logging.basicConfig(level=logging.DEBUG)

    # Create a BloxOne DDI Object
    b1ddi = bloxone.b1ddi()

    # Your can specify ini filename/path
    # b1ddi = bloxone.b1ddi('/Users/<username/<path>/<inifile>')

    # Show API Key
    b1ddi.api_key
    b1ddi.api_version

    # Generic Get wrapper using "Swagger Path for object"
    # response = b1ddi.get('<swagger path>')
    response = b1ddi.get('/ipam/ip_space')
    
    # Response object handling
    response.status_code
    response.text
    response.json()

    # Using custom parameters
    response = b1ddi.get('/dns/view', _fields="name,id")
    response.json()

    # Example using _filter
    response = b1ddi.get('/ipam/ip_space', _filter='name=="space-name"')

    # Example with multiple API parameters
    response = b1ddi.get('/ipam/subnet', _tfilter="Owner==marrison", _fields="address")
    response = b1ddi.get('/ipam/subnet', _tfilter="Owner~mar")

    # Get ID from key/value pair
    id = b1ddi.get_id('/dns/auth_zone', key="fqdn", value="home.")
    # Example Result: '80b0e234-8d5b-465b-8c98-e9430c5d83a9'

    id = b1ddi.get_id('/ipam/ip_space', key="name", value="marrison-lab", include_path=True)
    # 'ipam/ip_space/fd388619-b013-11ea-b956-ca543bd8c483'

    # Get DHCP Option IDs as a dictionary
    options = b1ddi.get_option_ids()
    options['43']
    # 'dhcp/option_code/44bbac08-c518-11ea-b9d9-06bf0d811d6d'

    # Get data for zone
    r = b1ddi.get_zone_child(parent="zone", name="home.", fields="name,record_type,record_data")

    # Get all on_prem_hosts
    # Create b1platform object
    b1p = bloxone.b1platform()
    response = b1p.on_prem_hosts()
    response.text

    # Using tag filters
    response = b1p.on_prem_hosts(_tfilter="Owner==marrison")
    response.text

    # Get all records for a 'named' zone
    response = b1ddi.get_zone_child(name="home.")
    response.text

    # Get all zones in a view by view name
    response = b1ddi.get_zone_child(name="marrison-dns-view1")
    response.text

    # Create Examples body = ( '{ "name": "my-ip-space", "tags": { "Owner":
                                "marrison" }}' )
    r = b1ddi.create('/ipam/ip_space', body=body) 
    r.text

    # '{"result":{"asm_config":{"asm_threshold":90,"enable":true,"enable_notification":true,"forecast_period":14,"growth_factor":20,"growth_type":"percent","history":30,"min_total":10,"min_unused":10,"reenable_date":"1970-01-01T00:00:00Z"},"asm_scope_flag":0,"comment":"","dhcp_config":{"allow_unknown":true,"filters":[],"ignore_list":[],"lease_time":3600},"dhcp_options":[],"id":"ipam/ip_space/edfb2cde-c2fc-11ea-b5c8-3670d2b79356","inheritance_sources":null,"name":"marrison-test","tags":null,"threshold":{"enabled":false,"high":0,"low":0},"utilization":{"abandon_utilization":0,"abandoned":"0","dynamic":"0","free":"0","static":"0","total":"0","used":"0","utilization":0}}}'

    r = b1ddi.get_object_by_key('/ipam/ip_space', key="name", value="marrison-lab")
    r.text
    # '{"result":{"asm_config":{"asm_threshold":90,"enable":true,"enable_notification":true,"forecast_period":14,"growth_factor":20,"growth_type":"percent","history":30,"min_total":10,"min_unused":10,"reenable_date":"1970-01-01T00:00:00Z"},"asm_scope_flag":0,"comment":"","dhcp_config":{"allow_unknown":true,"filters":[],"ignore_list":[],"lease_time":43200},"dhcp_options":[],"id":"ipam/ip_space/fd388619-b013-11ea-b956-ca543bd8c483","inheritance_sources":null,"name":"marrison-lab","tags":{"Location":"Hampshire, UK","Owner":"marrison"},"threshold":{"enabled":false,"high":0,"low":0},"utilization":{"abandon_utilization":0,"abandoned":"0","dynamic":"40","free":"65491","static":"5","total":"65536","used":"45","utilization":0}}}'
     

    # Update tags on an on_prem_hosts object example
    # Create a b1platform object
    b1p = bloxone.b1platform('/Users/marrison/bin/tide.ini')
    # Note: this will change the "tags" i.e. replace the "tags" with the "tags" in the update body
    body = '{"display_name":"marrison-hw-ddi1", "tags":{"Location":"Hampshire, UK","Owner":"marrison","host/deployment_type":"APPLIANCE","host/k8s":"false","host/ophid":"63f2b1c3f80455d87186aa054e87f1a9"}}'
    # Call the update method
    response = b1p.update('/on_prem_hosts', id="97290", body=body)
