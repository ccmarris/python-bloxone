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
__version__ = '0.1.2'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import bloxone
import logging
import json
import os
import re
import datetime
import ipaddress

# ** Global Vars **

class b1ddi(bloxone.b1):

    # Generic Methods
    def get(self, objpath, id="", action="", **params):
        '''
        Generic get object wrapper for ddi objects

        Parameters:
            objpath (str):  Swagger object path
            id (str):       Optional Object ID
            action (str):   Optional object action, e.g. "nextavailableip"
        
        Returns:
            response (obj): Requests response object
        '''
        # Build url
        url = self.ddi_url + objpath
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        response = self._apiget(url)

        return response


    def get_id(self, objpath, *, key="", value="", include_path=False):
        '''
        Get object id using key/value pair

        Parameters:
            objpath (str):  Swagger object path
            key (str):      name of key to match
            value (str):    value to match

        Returns:
            id (str):   object id or ""
        '''

        # Local Variables
        id=""

        # Build url
        url = self.ddi_url + objpath
        url = url + '?_fields=' + key + ',id'

        # Make API Call
        response = self._apiget(url)

        # Process response
        if response.status_code in self.return_codes_ok:
            objs = json.loads(response.text)
            # Look for results
            if "results" in objs.keys():
                for obj in objs['results']:
                    if obj[key] == value:
                        id = obj['id']
                        if not include_path:
                            id = id.rsplit('/',1)[1]
                if not id:
                    logging.debug("Key {} with value {} not found."
                                  .format(key,value))
            else:
                id = ""
                logging.debug("No results found.")
        else:
            id=""
            logging.debug("HTTP Error occured. {}".format(response.status_code))
        logging.debug("id: {}".format(id)) 

        return id


    def create(self, objpath, body=""):
        '''
        Generic create object wrapper for ddi objects

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response (obj): Requests response object
        '''
        # Build url
        url = self.ddi_url + objpath

        # Make API Call
        response = self._apipost(url, body)

        return response


    def delete(self, objpath, id=""):
        '''
        Generic delete object wrapper for ddi objects

        Parameters:
            objpath (str):  Swagger object path
            id (str):       Object id to delete

        Returns:
            response (obj): Requests response object
        '''
        # Build url
        url = self.ddi_url + objpath
        url = self._use_obj_id(url,id=id)

        # Make API Call
        response = self._apidelete(url)

        return response


    # *** Helper Methods ***
    # *** IPAM ***

    def get_ip_space(self, id="", **params):
        '''
        Method to retrieve IP Spaces

        Parameters:
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''
        return self.get('/ipam/ip_space', id=id, **params)


    def create_ip_space(self, **params):
        '''
        Method to create IP Space

        Parameters:
            **params (dict): Generic API parameters

        Returns:
        create_ip_space = self.ip_space(body="hello")
        '''
        return self.create(id, **params)


    def get_address_block(self, id="", action="", **params):
        '''
        Method to retrieve address block

        Parameters:
            id (str):       BloxOne object id
            nextip (bool):  Get nextavailableip for obj
                            ignored if id not specified
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''

        # Call BloxOne API GET Method
        return self.get('/ipam/address_block', id=id, action=action, **params)


    def get_subnet(self, id="", action="", **params):
        '''
        Method to retrieve subnets

        Parameters:
            id (str):       BloxOne object id
            nextip (bool):  Get nextavailableip for obj
                            ignored if id not specified
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''
        
        # Call BloxOne API GET Method
        return self.get('/ipam/subnet', id=id, action=action, **params)

    # *** DHCP ***

    def get_range(self, id="", action="", **params):
        '''
        Method to retrieve DHCP Ranges

        Parameters:
            id (str):       BloxOne object id
            nextip (bool):  Get nextavailableip for obj
                            ignored if id not specified
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''
        
        # Call BloxOne API GET Method
        return self.get('/ipam/range', id=id, action=action, **params)


    def get_lease(self, **params):
        '''
        Method to retrieve Leases

        Parameters:
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''
        
        # Call BloxOne API GET Method
        return self.get('/dhcp/lease', **params)


    # *** DNS ***
    
    def get_dns_views(self, id="", **params):
        '''
        Method to retrieve DNS Views

        Parameters:
            id (str):       BloxOne object id
            nextip (bool):  Get nextavailableip for obj
                            ignored if id not specified
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''

        # Call BloxOne API GET Method
        return self.get('/dns/view', id=id, **params)


    def get_auth_zones(self, id="", **params):
        '''
        Method to retrieve DNS Zones

        Parameters:
            id (str):       BloxOne object id
            nextip (bool):  Get nextavailableip for obj
                            ignored if id not specified
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''
        
        # Call BloxOne API GET Method
        return self.get('/dns/auth_zone', id=id, **params)

    def get_dns_servers(self, id="", **params):
        '''
        Method to retrieve DNS servers

        Parameters:
            id (str):       BloxOne object id
            nextip (bool):  Get nextavailableip for obj
                            ignored if id not specified
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''
        
        # Call BloxOne API GET Method
        return self.get('/dns/dns_servers', id=id, **params)


    def get_auth_nsg(self, id="", **params):
        '''
        Method to retrieve DNS Nameserver Groups

        Parameters:
            id (str):       BloxOne object id
            nextip (bool):  Get nextavailableip for obj
                            ignored if id not specified
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''

        # Call BloxOne API GET Method
        return self.get('/dns/auth_nsg', id=id, **params)


    def get_forward_zone(self, id="", **params):
        '''
        Method to retrieve DNS Zones

        Parameters:
            id (str):       BloxOne object id
            nextip (bool):  Get nextavailableip for obj
                            ignored if id not specified
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''
        
        # Call BloxOne API GET Method
        return self.get('/dns/auth_nsg', id=id, **params)

    def get_forward_nsg(self, id="", **params):
        '''
        Method to retrieve DNS Zones

        Parameters:
            id (str):       BloxOne object id
            nextip (bool):  Get nextavailableip for obj
                            ignored if id not specified
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''
        
        # Call BloxOne API GET Method
        return self.get('/dns/auth_nsg', id=id, **params)


    # *** Undocumented DNS Calls ***

    def get_zone_child(self, parent="zone", name="", id="", fields=""):
        '''
        Method to retrieve Zones in specified view

        Parameters:
            name (str): BloxOne object id
            id (str):   BloxOne object id
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''
        if name and not id:
            if parent == "view":
                id = self.get_id('/dns/view', key="name", value=name)
                # result = self.get('/dns/view', _fields="name,id")
                # logging.debug(result.text)
            elif parent == "zone":
                id = self.get_id('/dns/auth_zone', key="fqdn", value=name)
                result = self.get('/dns/auth_zone', _fields="fqdn,id")
                logging.debug(result.text)
            objs = json.loads(result.text)
            if "results" in objs.keys():
                for obj in objs['results']:
                    if obj['fqdn'] == name:
                        id = obj['id']
            else:
                id = ""
            logging.debug("id: {}".format(id)) 
        # Build URL
        objpath = '/dns/zone_child' + '?_filter=parent=="' + id + '"'
        if fields:
            objpath = objpath + '&_fields=' + fields
        logging.debug("Objectpath: {}".format(objpath))
        
        # Call BloxOne API GET Method
        return self.get(objpath)
        