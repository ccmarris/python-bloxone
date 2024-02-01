#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 BloxOne Threat Defense Enpoint API Wrapper Class and Helpers

 Author: Chris Marrison

 Date Last Updated: 20240201

 Todo:

 Copyright (c) 2020 - 2024 Chris Marrison / Infoblox

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
__version__ = '0.2.1'
__author__ = 'Chris Marrison/Krishna Vasudeva'
__author_email__ = 'chris@infoblox.com'

import bloxone
import logging

# ** Global Vars **

class b1tdlad(bloxone.b1):

    # Generic Methods
    def get(self, objpath, **params):
        '''
        Generic get object wrapper for Threat Defense objects

        Parameters:
            objpath (str):  Swagger object path
            id (str):       Optional Object ID
            action (str):   Optional object action, e.g. "nextavailableip"
        
        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.tdlad_url + objpath
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        response = self._apiget(url)

        return response


    def update(self, objpath, id="", body=""):
        '''
        Generic create object wrapper 

        Parameters:
            objpath (str):  Swagger object path
            body (str): JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url if needed
        url = self.tdlad_url + objpath
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apiput(url, body)

        return response
    

    def get_lookalikes(self, target_domain='', format='json', **params):
        '''
        '''
        result = None

        url = f'{self.tdlad_url}/lookalikes'
        if target_domain:
            filter = f'targetdomain=="{target_domain}"'
            url = self._add_params(url, _filter=filter)
            url = self._add_params(url, first_param=False, **params)
        else:
            url = self._add_params(url, **params)
        
        response = self._apiget(url)
        if response.status_code in self.return_codes_ok:
            result = response.json()
        
        return result

