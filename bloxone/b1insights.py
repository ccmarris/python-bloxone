#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 BloxOne Threat Defence API Wrapper Class and Helpers

 Author: Chris Marrison

 Date Last Updated: 20240701

 Todo:

 Copyright (c) 2020-2021 Chris Marrison / Infoblox

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
__version__ = '0.0.1'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import bloxone
import logging
import datetime
import json


# b1td class
class b1insights(bloxone.b1):
    '''
    BloxOne ThreatDefence API Wrapper
    Covers TIDE and Dossier
    '''

    # Generic Methods
    def get(self, objpath, **params):
        '''
        Generic get object wrapper for TIDE data objects

        Parameters:
            objpath (str):  Swagger object path
            action (str):   Optional object action
        
        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.insights_url + objpath
        url = self._use_obj_id(url, id=id)
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        response = self._apiget(url)

        return response


    def update(self, objpath, id="", body=""):
        '''
        Generic create object wrapper for insights objects

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.insights_url + objpath
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apiput(url, body)

        return response


   # *** Helper Methods ***

    def actor_insights(self, id=""):
        '''
        '''
        return self.get('/actor-insights', id=id)
        
    
    def config_insights(self, id=""):
        '''
        '''
        return self.get('/config-insights/analytics', id=id)


    def policy_check(self):
        '''
        '''
        return self.get('/config-insights/policy-check')
    

    def insights(self, id="", action=""):
        '''
        '''
        return self.get('/insights', id=id, action=action)


    def update_status(self, body=""):
        return self.update('/insights/status', body="")