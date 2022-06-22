#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 BloxOne DDI API Wrapper Class and Helpers

 Author: Chris Marrison

 Date Last Updated: 20220323

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
__version__ = '0.2.5'
__author__ = 'Chris Marrison/Krishna Vasudevan'
__author_email__ = 'chris@infoblox.com'

import bloxone
import logging
import json
from requests.models import Response

# ** Global Vars **

class b1tdc(bloxone.b1):
    '''
    BloxOne ThreatDefence Cloud API Wrapper
    '''

    # Generic Methods
    def get(self, objpath, id="", action="", **params):
        '''
        Generic get object wrapper for Threat Defense Cloud

        Parameters:
            objpath (str):  Swagger object path
            action (str):   Optional object action
        
        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.tdc_url + objpath
        if id:
            url = self._use_obj_id(url, id=id)
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        response = self._apiget(url)

        return response


    def post(self, objpath, body=""):
        '''
        Generic create object wrapper for Threat Defense Cloud

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.tdc_url + objpath

        # Make API Call
        response = self._apipost(url, body)

        return response


    def create(self, objpath, body=""):
        '''
        Generic create object wrapper for Threat Defense Cloud

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.tdc_url + objpath

        # Make API Call
        response = self._apipost(url, body)

        return response


    def delete(self, objpath, id="", body=""):
        '''
        Generic delete object wrapper for Threat Defense Cloud

        Parameters:
            objpath (str):  Swagger object path
            id (str):       Object id to delete
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.tdc_url + objpath
        if id:
            url = self._use_obj_id(url, id=id)

        # Make API Call
        response = self._apidelete(url, body)

        return response

       
    def put(self, objpath, id="", body=""):
        '''
        Generic put object wrapper for Threat Defense Cloud

        Parameters:
            objpath (str):  Swagger object path
            id (str):       Object id to update
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.tdc_url + objpath
        url = self._use_obj_id(url, id=id)

        # Make API Call
        response = self._apiput(url, body)

        return response


    def update(self, objpath, id="", body=""):
        '''
        Generic create object wrapper for Threat Defense Cloud

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.tdc_url + objpath
        url = self._use_obj_id(url, id=id)

        # Make API Call
        response = self._apipatch(url, body)

        return response

 
   # *** Helper Methods ***

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
        url = self.tdc_url + objpath
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
                        if not include_path and "/" in str(id):
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


    def get_object_by_key(self, objpath, *, key="", value="", include_path=False):
        '''
        Get object using key/value pair

        Parameters:
            objpath (str):  Swagger object path
            key (str):      name of key to match
            value (str):    value to match

        Returns:
            id (str):   object id or ""
        '''
        return self.get(objpath, id=self.get_id(objpath, key=key, value=value))


    def get_custom_lists(self, **params):
        '''
        Get custom lists

        Parameters:
            Additional parameters per API documentation
             
        Returns:
            response object: Requests response object
        '''
        url = self.tdc_url + '/named_lists'
        url = self._add_params(url, **params)

        # Make API Call
        response = self._apiget(url)

        return response


    def get_custom_list(self, name='', **params):
        '''
        Get the named custom list

        Parameters:
            name (str): Name of custom list
        
        Returns:
            response object: Requests response object
        '''
        id = self.get_id('/named_lists', key='name', value=name)
        if id:
            logging.debug(f'Custom list: {name} with id {id} found.')
            response = self.get('/named_lists', id=id, **params)
        else:
            logging.debug(f'Custom list: {name} not found.')
            response = self._not_found_response('named_list')

        return response


    def create_custom_list(self, name='', 
                                 confidence='HIGH', 
                                 items=[], 
                                 items_described=[]):
        '''
        Create deny custom lists

        Parameters:
            name (str): Name of custom list
            confidence (str): Confidence level
            items (list): List of indicators
            items_described (list): List of {"description": "", "item": ""}
        
        Note: 
            if items and items_described are both included items_described 
            will take precidence.

        Returns:
            response object: Requests response object
        '''
        if items:
            body = { "name": name,
                     "type": "custom_list",
                     "confidence_level": confidence,
                     "items": items }
        elif items_described:
            body = { "name": name,
                     "type": "custom_list",
                     "confidence_level": confidence,
                     "items_described": items_described }
        else:
            body = { "name": name,
                     "type": "custom_list",
                     "confidence_level": confidence }

        logging.debug("Body:{}".format(body))
        response = self.create('/named_lists', body=json.dumps(body))

        return response


    def add_items_to_custom_list(self, name='', items=[], items_described=[]):
        '''
        Add items to an existing custom list

        Parameters:
            name (str): Name of custom list
            items (list): List of indicators
            items_described (list): List of {"description": "", "item": ""}
        
        Note: 
            For updates both items and items_described can be included.

        Returns:
            response object: Requests response object
        '''
        body = {}
        id = self.get_id('/named_lists', key='name', value=name)
        if id:
            logging.debug(f'Custom list: {name} with id {id} found.')
            request = f'/named_lists/{id}/items'
            if items:
                body = { "items": items }
            if items_described:
                body.update( { "items_described": items_described } )

            logging.debug("Body:{}".format(body))
            response = self.post(request, body=json.dumps(body))
        else:
            logging.debug(f'Custom list: {name} not found.')
            response = self._not_found_response('named_list')

        return response


    def delete_items_from_custom_list(self, name='', 
                                            items=[], 
                                            items_described=[]):
        '''
        Delete items to an existing custom list

        Parameters:
            name (str): Name of custom list
            items (list): List of indicators
            items_described (list): List of {"description": "", "item": ""}
        
        Note: 
            For updates both items and items_described can be included.

        Returns:
            response object: Requests response object
        '''
        body = {}
        id = self.get_id('/named_lists', key='name', value=name)
        if id:
            logging.debug(f'Custom list: {name} with id {id} found.')
            request = f'/named_lists/{id}/items'
            if items:
                body = { "items": items }
            if items_described:
                body.update( { "items_described": items_described } )

            logging.debug("Body:{}".format(body))
            response = b1tdc.delete(request, body=json.dumps(body))
        else:
            logging.debug(f'Custom list: {name} not found.')
            response = self._not_found_response('named_list')

        return response

 
    def delete_custom_lists(self, names=[]):
        '''
        Delete custom list
            
        Parameters:
            name (list): List of names(str) to delete
        
        Returns:
            response object: Requests response object or None
        '''
        ids = []
        for name in names:
            id = self.get_id('/named_lists', key="name", value=name)
            if id:
                logging.debug(f'Custom list: {name} with id {id} found.')
                ids.append(str(id))
            else:
                logging.debug(f'Custom list: {name} not found.')
        if ids:
            body = { 'ids': ids }
            logging.debug("Body:{}".format(body))
            response = self.delete('/named_lists', body=json.dumps(body))
        else:
            logging.warning('No custom lists found')
            response = self._not_found_response('named_list')
        
        return response