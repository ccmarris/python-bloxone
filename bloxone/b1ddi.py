#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 BloxOne DDI API Wrapper Class and Helpers

 Author: Chris Marrison

 Date Last Updated: 20210803

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
__version__ = '0.4.5'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import bloxone
import logging
import json

# ** Global Vars **

class b1ddi(bloxone.b1):
    '''
    BloxOne DDI API Wrapper Class
    '''

    # Generic Methods
    def get(self, objpath, id="", action="", **params):
        '''
        Generic get object wrapper for ddi objects

        Parameters:
            objpath (str):  Swagger object path
            id (str):       Optional Object ID
            action (str):   Optional object action, e.g. "nextavailableip"
        
        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.ddi_url + objpath
        url = self._use_obj_id(url, id=id, action=action)
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        response = self._apiget(url)

        return response


    def post(self, objpath, id="", action="", body="", **params):
        '''
        Generic POST object wrapper for ddi objects

        Parameters:
            objpath (str):  Swagger object path
            id (str):       Optional Object ID
            action (str):   Optional object action, e.g. "nextavailableip"
            body (str):     JSON formatted data payload
        
        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.ddi_url + objpath
        url = self._use_obj_id(url, id=id, action=action)
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        response = self._apipost(url, body)

        return response


    def create(self, objpath, body=""):
        '''
        Generic create object wrapper for ddi objects

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.ddi_url + objpath
        logging.debug("URL: {}".format(url))

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
            response object: Requests response object
        '''
        # Build url
        url = self.ddi_url + objpath
        url = self._use_obj_id(url,id=id)
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
            response object: Requests response object
        '''
        # Build url
        url = self.ddi_url + objpath
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apiput(url, body)

        return response


    def replace(self, objpath, id="", body=""):
        '''
        Generic create object wrapper for ddi objects

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.ddi_url + objpath
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

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
            include_path (bool): Include path to object id

        Returns:
            id (str):   object id or ""
        '''

        # Local Variables
        id = ""
        filter = key+'=="'+value+'"'
        fields = key + ',id'

        # Make API Call
        response = self.get(objpath, _filter=filter, _fields=fields)

        # Process response
        if response.status_code in self.return_codes_ok:
            obj = response.json()
            # Look for results
            if "results" in obj.keys():
                obj = obj['results']
                if obj:
                    id = obj[0]['id']
                    if not include_path:
                        id = id.rsplit('/',1)[1]
                else:
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


    def search_response(self, response, key="", value="", include_path=False):
        '''
        Get object id using key/value pair by searching a 
        Request response object.

        Parameters:
            response object:     Request response obj
            key (str):          name of key to match
            value (str):        value to match
            include_path (bool): Include path to object id

        Returns:
            id (str):   object id or ""
        '''

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


    def get_option_ids(self, option_space=""):
        '''
        Return a dictionary of DHCP Option IDs
        Based on idea/code from John Neerdael

        Parameters:
            option_space (str): Optional Option Space ID
        
        Returns:
            option_ids (dict): Dictionary keyed on option number of ids
        '''
        option_ids = {}

        response = self.get('/dhcp/option_code', _fields='code,id')
        if response.status_code in self.return_codes_ok:
            if 'results' in response.json().keys():
                optioncodes = response.json()['results']
                for item in optioncodes:
                    code = item['code']
                    id = item['id']
                    option_ids.update({ code: id })
        
        return option_ids


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


    def add_tag(self, objpath, id, tagname="", tagvalue=""):
        '''
        Method to add a tag to an existing object
        Note: PUT/update Not Implemented in API as yet

        Parameters:
            objpath (str):  Swagger object path
            id (str): Object ID
            tagname (str): Name of tag to add
            tagvalue (str): Value to associate with tag

        Returns:
            response object: Requests response object
        '''
        response = self.get(objpath, id=id, _fields='tags')
        if response.status_code in self.return_codes_ok:
            data = response.json()['result']
        else:
            data = {}
        logging.debug("Existing tags: {}".format(data['tags']))
        if data:
            # Add new tag to data
            if tagname:
                data['tags'].update({tagname: tagvalue})
                logging.debug("New tags: {}".format(data['tags']))
            # Update object
            response = self.replace(objpath, id=id, body=json.dumps(data))
        else:
            logging.debug("No object found")

        return response


    def delete_tag(self, objpath, id="", tagname=""):
        '''
        Method to delete a tag from an existing On Prem Host

        Parameters:
            objpath (str):  Swagger object path
            tagname (str): Name of tag to add

        Returns:
            response object: Requests response object
        '''
        # tags = self.get_tags('/on_prem_hosts', id=id)
        response = self.get(objpath, id=id, _fields='tags')
        if response.status_code in self.return_codes_ok:
            data = response.json()['result']
            logging.debug("Existing tags: {}".format(data['tags']))
            # Delete tag from data
            if tagname in data['tags'].keys():
                data['tags'].pop(tagname, True)
                logging.debug("New tags: {}".format(data['tags']))
                # Update object
                response = self.replace(objpath, id=id, body=json.dumps(data))

        return response


    # *** Undocumented DNS Calls ***

    def get_zone_child(self, parent="zone", name="", id="", fields=""):
        '''
        Method to retrieve Zones in specified view

        Parameters:
            name (str): BloxOne object id
            id (str):   BloxOne object id
            **params (dict): Generic API parameters

        Returns:
           response object: Requests response object
        '''
        if name and not id:
            if parent == "view":
                id = self.get_id('/dns/view', key="name", value=name, include_path=True)
                # result = self.get('/dns/view', _fields="name,id")
                # logging.debug(result.text)
            elif parent == "zone":
                id = self.get_id('/dns/auth_zone', key="fqdn", value=name, include_path=True)
                # result = self.get('/dns/auth_zone', _fields="fqdn,id")
                # logging.debug(result.text)
            logging.debug("id: {}".format(id)) 
        # Build URL
        objpath = '/dns/zone_child' + '?_filter=parent=="' + id + '"'
        if fields:
            objpath = objpath + '&_fields=' + fields
        logging.debug("Objectpath: {}".format(objpath))
        
        # Call BloxOne API GET Method
        return self.get(objpath)
        
