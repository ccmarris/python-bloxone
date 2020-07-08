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

import logging
import os
import re
import configparser
import datetime
import ipaddress
import requests
import urllib.parse

# ** Global Vars **
cspurl = "https://csp.infoblox.com/api"


# ** Facilitate TIDE Config File for API Key **

def read_b1_ini(ini_filename):
    '''
    Open and parse ini file

    Parameters:
        ini_filename (str): name of inifile

    Returns:
        config (dict): Dictionary of BloxOne configuration elements

    '''
    # Local Variables
    cfg = configparser.ConfigParser()
    config = {}
    ini_keys = ['url', 'api_version', 'api_key']

    # Attempt to read api_key from ini file
    try:
        cfg.read(ini_filename)
    except configparser.Error as err:
        logging.error(err)

    # Look for TIDE section
    if 'BloxOne' in cfg:
        for key in ini_keys:
            # Check for key in BloxOne section
            if key in cfg['BloxOne']:
                config[key] = cfg['BloxOne'][key].strip("'\"")
                logging.debug('Key {} found in {}: {}'.format(key, ini_filename, config[key]))
            else:
                logging.warn('Key {} not found in BloxOne section.'.format(key))
                config[key] = ''
    else:
        logging.warn('No BloxOne Section in config file: {}'.format(ini_filename))
        config['api_key'] = ''

    return config


class b1:
    '''
    Class to simplify access to the BloxOne APIs
    '''

    def __init__(self, cfg_file='config.ini'):
        '''
        Read ini file and set attributes

        Parametrers:
            cfg_file (str): Override default ini filename

        '''

        self.cfg = {}

        # Read ini file
        self.cfg = read_b1_ini(cfg_file)

        # Define generic header
        self.headers = ( {'content-type': 'application/json',
                        'Authorization': 'Token ' + self.cfg['api_key']} )
        
        # Create base URLs
        # self.ep_url = self.cfg['url'] + '/api/host_app/' + self.cfg['api_version']
        # self.fw_url = self.cfg['url'] + '/api/host_app/' + self.cfg['api_version']
        self.host_url = self.cfg['url'] + '/api/host_app/' + self.cfg['api_version']
        self.dns_url = self.cfg['url'] + '/api/ddi/' + self.cfg['api_version'] + '/dns'
        self.ipam_url = self.cfg['url'] + '/api/ddi/' + self.cfg['api_version'] + '/ipam'
        self.dhcp_url = self.cfg['url'] + '/api/ddi/' + self.cfg['api_version'] +'/dhcp'

        return


    def _add_params(self, url, params):
        # Add params to API call URL
        if len(params):
            first_param = True
            for param in params.keys():
               if first_param:
                   url = url + '?'
                   first_param = False
               else:
                   url = url + '&'
               url = url + param + '=' + params[param]
        
        return url


    def _apiget(self, url):    
     # Call BloxOne API
        try:
            response = requests.request("GET",
                                        url,
                                        headers=self.headers)
        # Catch exceptions
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return 0, "Exception occured."

        # Return response code and body text
        # return response.status_code, response.text
        return response


    def _apipost(self, url, body):    
     # Call BloxOne API
        try:
            response = requests.request("POST",
                                        url,
                                        headers=self.headers,
                                        data=body)
        # Catch exceptions
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return 0, "Exception occured."

        # Return response code and body text
        return response

 
    def _apidelete(self, url):    
     # Call BloxOne API
        try:
            response = requests.request("DELETE",
                                        url,
                                        headers=self.headers)
        # Catch exceptions
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return 0, "Exception occured."

        # Return response code and body text
        return response


    '''
    __To Do__

    def apiput(self, url, body):    
     # Call BloxOne API
        try:
            response = requests.request("PUT",
                                        url,
                                        headers=self.headers,
                                        body)
        # Catch exceptions
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return 0, "Exception occured."

        # Return response code and body text
        return response.status_code, response.text

 
    def _apipatch(self, url, body):    
     # Call BloxOne API
        try:
            response = requests.request("PATCH",
                                        url,
                                        headers=self.headers,
                                        body)
        # Catch exceptions
        except requests.exceptions.RequestException as e:
            logging.error(e)
            return 0, "Exception occured."

        # Return response code and body text
        return response

    '''

    def _use_obj_id(self, url, id="", nextip=False):
        '''
        Update URL for use with object id
        
        Parameters:
            id (str): Bloxone Object id
            nextip (bool): use nextavailableip

        Returns:
            url (str): Updated url
        '''
        # Check for id and next available IP
        if id:
            url = url + '/' + id
            if nextip:
                url = url + '/nextavailableip'
        
        return url


    # *** Platform API Requests *** 

    def on_prem_hosts(self, **params):
        '''
        Method to retrieve On Prem Hosts
        (undocumented)

        Parameters:
            **params (dict): Generic API parameters

        Returns:
           status_code (obj): status code or zero on exception
           body (str): Raw JSON or "Exception occurred." upon exception
        '''

        # Build URL
        url = self.host_url + '/on_prem_hosts'
        url = self._add_params(url, params)
        
        # Call BloxOne API
        response = self._apiget(url)

        # Return response code and body text
        return response 

