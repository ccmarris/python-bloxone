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
__version__ = '0.0.5'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import bloxone
import logging
import os
import re
import datetime
import ipaddress

# ** Global Vars **

class b1ddi(bloxone.b1):

    # *** IPAM ***

    def _ip_space(self, id="", body="", **params):
        '''
        Method to retrieve IP Spaces

        Parameters:
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''
        # Build URL
        url = self.ipam_url + '/ip_space'
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, params)
        
        if body:
            response = "Hello"
        else:
            # Call BloxOne API GET Method
            response = self._apiget(url)
        
        
        # Return response code and response text
        return response
    

    def get_ip_space(self, id="", **params):
        '''
        Method to retrieve IP Spaces

        Parameters:
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''
        return self._ip_space(id,params)


    def create_ip_space(self):
        '''
        Method to create IP Space

        Parameters:
            **params (dict): Generic API parameters

        Returns:
        create_ip_space = self.ip_space(body="hello")
        '''
        return self._ip_space(id,params)


    def address_block(self, id="", nextip=False, **params):
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
        # Build URL
        url = self.ipam_url + '/address_block'
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, params)
        
        # Call BloxOne API GET Method
        response, response = self._apiget(url)
        
        # Return response code and response text
        return response


    def subnet(self, id="", nextip=False, **params):
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
        # Build URL
        url = self.ipam_url + '/subnet'
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, params)
        
        # Call BloxOne API GET Method
        response, response = self._apiget(url)
        
        # Return response code and response text
        return response, response

    # *** DHCP ***

    def dhcp_range(self, id="", nextip=False, **params):
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
        # Build URL
        url = self.ipam_url + '/range'
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, params)
        
        # Call BloxOne API GET Method
        response, response = self._apiget(url)
        
        # Return response code and response text
        return response, response


    def leases(self, **params):
        '''
        Method to retrieve Leases

        Parameters:
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''
        # Build URL
        url = self.dhcp_url + '/lease'
        url = self._add_params(url, params)
        
        # Call BloxOne API GET Method
        response, response = self._apiget(url)
        
        # Return response code and response text
        return response, response


    # *** DNS ***
    
    def dns_views(self, id="", **params):
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
        # Build URL
        url = self.dns_url + '/view'
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, params)
        
        # Call BloxOne API GET Method
        response, response = self._apiget(url)
        
        # Return response code and response text
        return response, response


    def auth_zones(self, id="", **params):
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
        # Build URL
        url = self.dns_url + '/auth_zone'
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, params)
        
        # Call BloxOne API GET Method
        response, response = self._apiget(url)
        
        # Return response code and response text
        return response, response


    def dns_servers(self, id="", **params):
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
        # Build URL
        url = self.dns_url + '/server'
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, params)
        
        # Call BloxOne API GET Method
        response, response = self._apiget(url)
        
        # Return response code and response text
        return response, response


    def auth_nsg(self, id="", **params):
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
        # Build URL
        url = self.dns_url + '/auth_nsg'
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, params)
        
        # Call BloxOne API GET Method
        response, response = self._apiget(url)
        
        # Return response code and response text
        return response, response


    def forward_zone(self, id="", **params):
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
        # Build URL
        url = self.dns_url + '/auth_zone'
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, params)
        
        # Call BloxOne API GET Method
        response, response = self._apiget(url)
        
        # Return response code and response text
        return response, response

    def forward_nsg(self, id="", **params):
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
        # Build URL
        url = self.dns_url + '/auth_zone'
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, params)
        
        # Call BloxOne API GET Method
        response, response = self._apiget(url)
        
        # Return response code and response text
        return response, response
    # Undocumented DNS Calls

    def zones_in_view(self, viewname="", viewid="", **params):
        '''
        Method to retrieve Zones in specified view

        Parameters:
            viewname (str): BloxOne object id
            viewid (str):   BloxOne object id
            **params (dict): Generic API parameters

        Returns:
           response (obj): Requests response object
        '''
        # Build URL
        url = self.dns_url + '/zone_child'
        url = self._add_params(url, params)
        
        # Call BloxOne API GET Method
        response, response = self._apiget(url)
        
        # Return response code and response text
        return response, response

