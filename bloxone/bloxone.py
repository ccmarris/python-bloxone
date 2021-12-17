#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 Module to provide class hierachy to simplify access to the BloxOne APIs

 Date Last Updated: 20210713

 Todo:

    api_key format verification upon inifile read.

 Copyright (c) 2020 Chris Marrison / Infoblox

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
import logging
import configparser
import requests
import os
import re
import json

# ** Global Vars **
__version__ = '0.8.5'
__author__ = 'Chris Marrison'
__email__ = 'chris@infoblox.com'
__doc__ = 'https://python-bloxone.readthedocs.io/en/latest/'
__license__ = 'BSD'


# Custom Exceptions
class IniFileSectionError(Exception):
    '''
    Exception for missing section in ini file
    '''
    pass

class IniFileKeyError(Exception):
    '''
    Exception for missing key in ini file
    '''
    pass

class APIKeyFormatError(Exception):
    '''
    Exception for API key format mismatch
    '''
    pass

# ** Facilitate ini file for basic configuration including API Key

def read_b1_ini(ini_filename):
    '''
    Open and parse ini file

    Parameters:
        ini_filename (str): name of inifile

    Returns:
        config (dict): Dictionary of BloxOne configuration elements

    Raises:
        IniFileSectionError
        IniFileKeyError
        APIKeyFormatError
        FileNotFoundError

    '''
    # Local Variables
    cfg = configparser.ConfigParser()
    config = {}
    ini_keys = ['url', 'api_version', 'api_key']
 
    # Check for inifile and raise exception if not found
    if os.path.isfile(ini_filename):
        # Attempt to read api_key from ini file
        try:
            cfg.read(ini_filename)
        except configparser.Error as err:
            logging.error(err)

        # Look for BloxOne section
        if 'BloxOne' in cfg:
            for key in ini_keys:
                # Check for key in BloxOne section
                if key in cfg['BloxOne']:
                    config[key] = cfg['BloxOne'][key].strip("'\"")
                    logging.debug('Key {} found in {}: {}'
                                 .format(key, ini_filename, config[key]))
                else:
                    logging.error('Key {} not found in BloxOne section.'
                                 .format(key))
                    raise IniFileKeyError('Key "' + key + '" not found within' 
                        '[BloxOne] section of ini file {}'.format(ini_filename))
                    
        else:
            logging.error('No BloxOne Section in config file: {}'
                         .format(ini_filename))
            raise IniFileSectionError('No [BloxOne] section found in ini file {}'
                                     .format(ini_filename))
        
        # Verify format of API Key
        if verify_api_key(config['api_key']):
            logging.debug('API Key passed format verification')
        else:
            logging.debug('API Key {} failed format verification'
                          .format(config['api_key']))
            raise APIKeyFormatError('API Key {} failed format verification'
                                    .format(config['api_key']))

    else:
        raise FileNotFoundError('ini file "{}" not found.'.format(ini_filename))

    return config


def verify_api_key(apikey):
    '''
    Verify format of API Key
    
    Parameters:
       apikey (str): api key

    Returns:
        bool: True is apikey passes format validation
    '''
    if re.fullmatch('[a-z0-9]{32}|[a-z0-9]{64}', apikey, re.IGNORECASE):
        status = True
    else:
        status = False

    return status


class b1:
    '''
    Parent Class to simplify access to the BloxOne APIs for subclasses
    Can also be used to genericallly access the API

    Raises:
        IniFileSectionError
        IniFileKeyError
        APIKeyFormatError
        FileNotFoundError
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
        self.api_key = self.cfg['api_key']
        self.headers = ( {'content-type': 'application/json',
                        'Authorization': 'Token ' + self.api_key} )
        
        # Create base URLs
        self.base_url = self.cfg['url']
        self.api_version = self.cfg['api_version']

        # B1 & B1DDI URLs
        self.anycast_url = self.base_url + '/api/anycast/' + self.cfg['api_version']
        self.authn_url = self.base_url + '/api/authn/' + self.cfg['api_version']
        self.bootstrap_url = self.base_url + '/bootstrap-app/' + self.cfg['api_version']
        self.cdc_url = self.base_url + '/api/cdc-flow/' + self.api_version
        self.diagnostics_url = self.base_url + '/diagnostic-service/' + self.api_version
        self.ddi_url = self.base_url + '/api/ddi/' + self.api_version
        self.host_url = self.base_url + '/api/host_app/' + self.cfg['api_version']
        self.notifications_url = self.base_url + '/atlas-notifications-config/'+ self.api_version
        self.sw_url = self.base_url + '/api/upgrade_policy/' + self.cfg['api_version']
        self.ztp_url = self.base_url + '/atlas-host-activation/' + self.cfg['api_version']
        
        # B1TD URLs
        self.tdc_url = self.base_url + '/api/atcfw/' + self.cfg['api_version']
        self.tdep_url = self.base_url + '/api/atcep/' + self.cfg['api_version']
        self.tddfp_url = self.base_url + '/api/atcdfp/' + self.cfg['api_version']
        self.tdlad_url = self.base_url + '/api/atclad/' + self.cfg['api_version']
        self.tide_url = self.base_url + '/tide/api' 
        self.dossier_url = self.base_url + '/tide/api/services/intel/lookup'
        self.threat_enrichment_url = self.base_url + '/tide/threat-enrichment'

        # Reporting URLs
        self.ti_reports_url = self.base_url + '/api/ti-reports/' + self.cfg['api_version']
        self.aggr_reports_url  = self.ti_reports_url + '/activity/aggregations'
        self.insights_url = self.aggr_reports_url + '/insight'
        self.sec_act_url = self.base_url + '/api/ti-reports/v1/activity/hits'

        # List of successful return codes
        self.return_codes_ok = [200, 201, 204]

        return


    def _add_params(self, url, first_param=True, **params):
        # Add params to API call URL
        if len(params):
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
            logging.debug("url: {}".format(url))
            raise

        # Return response code and body text
        # return response.status_code, response.text
        return response


    def _apipost(self, url, body, headers=""):    
        # Set headers
        if not headers:
            headers = self.headers
     
        # Call BloxOne API
        try:
            response = requests.request("POST",
                                        url,
                                        headers=headers,
                                        data=body)
        # Catch exceptions
        except requests.exceptions.RequestException as e:
            logging.error(e)
            logging.debug("url: {}".format(url))
            logging.debug("body: {}".format(body))
            raise

        # Return response code and body text
        return response

 
    def _apidelete(self, url, body=""):    
     # Call BloxOne API
        try:
            response = requests.request("DELETE",
                                        url,
                                        headers=self.headers,
                                        data=body)
        # Catch exceptions
        except requests.exceptions.RequestException as e:
            logging.error(e)
            logging.debug("URL: {}".format(url))
            logging.debug("BODY: {}".format(body))
            raise

        # Return response code and body text
        return response


    def _apiput(self, url, body):    
     # Call BloxOne API
        try:
            response = requests.request("PUT",
                                        url,
                                        headers=self.headers,
                                        data=body)
        # Catch exceptions
        except requests.exceptions.RequestException as e:
            logging.error(e)
            logging.debug("url: {}".format(url))
            logging.debug("body: {}".format(body))
            raise

        # Return response code and body text
        return response

 
    def _apipatch(self, url, body):    
        # Call BloxOne API
        try:
            response = requests.request("PATCH",
                                        url,
                                        headers=self.headers,
                                        data=body)
        # Catch exceptions
        except requests.exceptions.RequestException as e:
            logging.error(e)
            logging.debug("url: {}".format(url))
            logging.debug("body: {}".format(body))
            raise

        # Return response code and body text
        return response


    def _use_obj_id(self, url, id="", action=""):
        '''
        Update URL for use with object id
        
        Parameters:
            id (str): Bloxone Object id
            action (str): e.g. nextavailableip

        Returns:
            string : Updated url
        '''
        # Check for id and next available IP
        if id:
            url = url + '/' + id
            if action:
                url = url + '/' + action
        else:
            if action:
                logging.debug("Action {} not supported without " 
                              "a specified object id.")
        
        return url


    # Public Generic Methods
    def get(self, url, id="", action="", **params):
        '''
        Generic get object wrapper 

        Parameters:
            url (str):      Full URL
            id (str):       Optional Object ID
            action (str):   Optional object action, e.g. "nextavailableip"
        
        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self._use_obj_id(url, id=id, action=action)
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        response = self._apiget(url)

        return response


    def post(self, url, id="", action="", body="", **params):
        '''
        Generic Post object wrapper 

        Parameters:
            url (str):      Full URL
            id (str):       Optional Object ID
            action (str):   Optional object action, e.g. "nextavailableip"
        
        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self._use_obj_id(url, id=id, action=action)
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        response = self._apipost(url, body)

        return response


    def create(self, url, body=""):
        '''
        Generic create object wrapper 

        Parameters:
            url (str):  Full URL
            body (str): JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apipost(url, body)

        return response


    def delete(self, url, id="", body=""):
        '''
        Generic delete object wrapper

        Parameters:
            url (str):  Full URL
            id (str):   Object id to delete
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        if id:
            url = self._use_obj_id(url,id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apidelete(url, body)

        return response


    def update(self, url, id="", body=""):
        '''
        Generic create object wrapper 

        Parameters:
            url (str):  Full URL
            body (str): JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url if needed
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apiput(url, body)

        return response


    def replace(self, url, id="", body=""):
        '''
        Generic create object wrapper 

        Parameters:
            url (str):  Full URL
            body (str): JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apipatch(url, body)

        return response