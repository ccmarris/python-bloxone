#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 Module to provide class hierachy to simplify access to the BloxOne APIs

 Date Last Updated: 20200820

 Todo:

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
__version__ = '0.5.3'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import logging
import configparser
import requests
import json

# ** Global Vars **
cspurl = "https://csp.infoblox.com/api"


# ** Facilitate ini file for basic configuration including API Key

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
    Parent Class to simplify access to the BloxOne APIs for subclasses
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
        self.ddi_url = self.base_url + '/api/ddi/' + self.api_version
        self.host_url = self.base_url + '/api/host_app/' + self.cfg['api_version']
        self.anycast_url = self.base_url + '/api/anycast/' + self.cfg['api_version']
        self.tdc_url = self.base_url + '/api/atcfw/' + self.cfg['api_version']
        self.tdep_url = self.base_url + '/api/atcep/' + self.cfg['api_version']
        self.tddfp_url = self.base_url + '/api/atcdfp/' + self.cfg['api_version']
        self.tdlad_url = self.base_url + '/api/atclad/' + self.cfg['api_version']
        self.tide_url = self.base_url + '/tide/api' 
        self.dossier_url = self.base_url + '/dossier/api' # Placeholder

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
            nextip (bool): use nextavailableip

        Returns:
            url (str): Updated url
        '''
        # Check for id and next available IP
        if id:
            url = url + '/' + id
            if action:
                url = url + '/' + action
        else:
            if action:
                logging.debug("Action {} not supported without " 
                              "a specified ovject id.")
        
        return url


class b1platform(b1):
    '''
    Class to simplify access to the BloxOne Platform APIs
    '''

    def get(self, objpath, id="", action="", **params):
        '''
        Generic get object wrapper for platform calls

        Parameters:
            objpath (str):  Swagger object path
            id (str):       Optional Object ID
            action (str):   Optional object action, e.g. "nextavailableip"

        Returns:
            response (obj): Requests response object
        '''

        # Build url
        url = self.host_url + objpath
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        response = self._apiget(url)

        return response

        
    def create(self, objpath, body=""):
        '''
        Generic create object wrapper for platform objects

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response (obj): Requests response object
        '''
        # Build url
        url = self.host_url + objpath
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apipost(url, body)

        return response


    def delete(self, objpath, id=""):
        '''
        Generic delete object wrapper for platform objects

        Parameters:
            objpath (str):  Swagger object path
            id (str):       Object id to delete

        Returns:
            response (obj): Requests response object
        '''
        # Build url
        url = self.host_url + objpath
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apidelete(url)

        return response


    def update(self, objpath, id="", body=""):
        '''
        Generic create object wrapper for ddi objects

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response (obj): Requests response object
        '''
        # Build url
        url = self.host_url + objpath
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apiput(url, body)

        return response


    def get_tags(self, objpath, id=""):
        '''
        Get tags for an object id

        Parameters:
            objpath (str):  Swagger object path

            id (str): id of object

        Returns:
            tags (dict): Dictionary of current tags
                         or empty dict if none
        
        .. todo::
            * make generic, however, this requires the below
            * Lookup dictionary of 'required fields' per object type
        '''
        tags = {}
        response = self.get(objpath, id=id, _fields="tags")
        if response.status_code in self.return_codes_ok:
            tags = json.loads(response.text)
            tags = tags['result']
        else:
            tags = {}
        
        return tags


    # *** Platform API Requests *** 

    def on_prem_hosts(self, **params):
        '''
        Method to retrieve On Prem Hosts
        (undocumented)

        Parameters:
            **params (dict): Generic API parameters

        Returns:
            response (obj): Requests response object
        '''

        # Call BloxOne API
        response = self.get('/on_prem_hosts', **params)

        # Return response object
        return response 


    def oph_add_tag(self, id="", tagname="", tagvalue=""):
        '''
        Method to add a tag to an existing On Prem Host

        Parameters:
            objpath (str):  Swagger object path
            tagname (str): Name of tag to add
            tagvalue (str): Value to associate

        Returns:
            response (obj): Requests response object
        '''
        # tags = self.get_tags('/on_prem_hosts', id=id)
        response = self.get('/on_prem_hosts', id=id, _fields="display_name,tags")
        if response.status_code in self.return_codes_ok:
            data = response.json()['result']
        else:
            data = {}
        logging.debug("Existing tags: {}".format(data))
        # Add new tag to data
        if tagname:
            data['tags'].update({tagname: tagvalue})
            logging.debug("New tags: {}".format(data))
        # Update object
        response = self.update('/on_prem_hosts', id=id, body=json.dumps(data))

        return response


    def oph_delete_tag(self, id="", tagname=""):
        '''
        Method to delete a tag from an existing On Prem Host

        Parameters:
            objpath (str):  Swagger object path
            tagname (str): Name of tag to add

        Returns:
            response (obj): Requests response object
        '''
        # tags = self.get_tags('/on_prem_hosts', id=id)
        response = self.get('/on_prem_hosts', id=id, _fields="display_name,tags")
        if response.status_code in self.return_codes_ok:
            data = response.json()['result']
            logging.debug("Existing tags: {}".format(data))
            # Delete tag from data
            if tagname in data['tags'].keys():
                data['tags'].pop(tagname, True)
                print(json.dumps(data))
                logging.debug("New tags: {}".format(data))
                # Update object
                response = self.update('/on_prem_hosts', id=id, body=json.dumps(data))

        return response