#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 Requirements:
   Python3 with re, ipaddress, requests and sqlite3 modules

 Author: Chris Marrison

 Date Last Updated: 20200605

 Todo:

 Copyright (c) 2018 Chris Marrison / Infoblox

 Redistribution and use in source and binary forms,
 with or without modification, are permitted provided
 that the following conditions are met:

 1. Redistributions of source code must retain the above copyright
 notice, this list of conditions and the following disclaimer.

 2. Redistributions in binary form must reproduce the above copyright
 notice, this list of conditions and the following disclaimer in the
 documentation and/or other materials provided with the distribution.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.

------------------------------------------------------------------------
'''
__version__ = '0.1.0'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import bloxone
import logging

log=logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)

# Create a BloxOne DDI Object
b1ddi = bloxone.b1ddi()
# Specify ini filename
# b1ddi = bloxone.b1ddi('/Users/<username/<path>/<inifile>')


# Generic Get wrapper using "Swagger Path for object"
response = b1ddi.get('/ipam/ip_space')
response.status_code
response.text
response.json()

response = b1ddi.get('/dns/view', _fields="name,id")
response.text

# Example with multiple API parameters
response = b1ddi.get('/ipam/subnet', _tfilter="Owner==marrison",_fields="address")

# Get ID from key/value pair

id = b1ddi.get_id('/dns/auth_zone', key="fqdn", value="home.")
# 'dns/auth_zone/80b0e234-8d5b-465b-8c98-e9430c5d83a9'
id = b1ddi.get_id('/ipam/ip_space', key="name", value="marrison_lab")

id = b1ddi.get_id('/ipam/ip_space', key="name", value="marrison-lab")
# 'ipam/ip_space/fd388619-b013-11ea-b956-ca543bd8c483'

r = b1ddi.get_zone_child(parent="zone", name="home.", fields="name,record_type,record_data")

# Example 'helper' methods

response = b1ddi.get_ip_space('_tfilter="Owner==marrison", _fields="name,id"')
response.text

# Undocumented Call Helpers

# Get all on_prem_hosts
response = b1ddi.on_prem_hosts()
response.text

# Using tag filters
response = b1ddi.on_prem_hosts(_tfilter="Owner==marrison")
response.text

# Get all records for a 'named' zone
response = b1ddi.get_zone_child(name="home.")
response.text

# Get all zones in a view by view name
response = b1ddi.get_zone_child(name="marrison-dns-view1")
response.text

# Create Examples

r = b1ddi.create('/ipam/ip_space', body=body)
r.text
# '{"result":{"asm_config":{"asm_threshold":90,"enable":true,"enable_notification":true,"forecast_period":14,"growth_factor":20,"growth_type":"percent","history":30,"min_total":10,"min_unused":10,"reenable_date":"1970-01-01T00:00:00Z"},"asm_scope_flag":0,"comment":"","dhcp_config":{"allow_unknown":true,"filters":[],"ignore_list":[],"lease_time":3600},"dhcp_options":[],"id":"ipam/ip_space/edfb2cde-c2fc-11ea-b5c8-3670d2b79356","inheritance_sources":null,"name":"marrison-test","tags":null,"threshold":{"enabled":false,"high":0,"low":0},"utilization":{"abandon_utilization":0,"abandoned":"0","dynamic":"0","free":"0","static":"0","total":"0","used":"0","utilization":0}}}'

>>> r = b1ddi.get_object_by_key('/ipam/ip_space', key="name", value="marrison-lab")
>>> r.text
'{"result":{"asm_config":{"asm_threshold":90,"enable":true,"enable_notification":true,"forecast_period":14,"growth_factor":20,"growth_type":"percent","history":30,"min_total":10,"min_unused":10,"reenable_date":"1970-01-01T00:00:00Z"},"asm_scope_flag":0,"comment":"","dhcp_config":{"allow_unknown":true,"filters":[],"ignore_list":[],"lease_time":43200},"dhcp_options":[],"id":"ipam/ip_space/fd388619-b013-11ea-b956-ca543bd8c483","inheritance_sources":null,"name":"marrison-lab","tags":{"Location":"Hampshire, UK","Owner":"marrison"},"threshold":{"enabled":false,"high":0,"low":0},"utilization":{"abandon_utilization":0,"abandoned":"0","dynamic":"40","free":"65491","static":"5","total":"65536","used":"45","utilization":0}}}'
>>> 
