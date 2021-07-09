#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 Module to provide class hierachy to simplify access to the BloxOne APIs

 Date Last Updated: 20210215

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
import bloxone
import logging
import requests
import json

# ** Global Vars **
__version__ = '0.7.1'
__author__ = 'Chris Marrison'
__email__ = 'chris@infoblox.com'
__doc__ = 'https://python-bloxone.readthedocs.io/en/latest/'
__license__ = 'BSD'


class b1platform(bloxone.b1oph):
    '''
    Class now reused for BloxOne Platform Methods, e.g. Audit Log
    Management of BloxOne On Prem Hosts is via the b1oph Class 
    b1oph class  is inherited here for compatibility
    '''

    def auditlog(self, **params):
        '''
        Get the audit log

        Parameters:
            **params (dict): Generic API parameters
        Returns:
            audit_log (list); list of dict
        '''
        # Local variables
        audit_log = []

        url = self.base_url + '/api/auditlog/' + self.api_version +'/logs'
        url = self._add_params(url, **params)

        logging.debug("URL: {}".format(url))

        # Call API
        response = self._apiget(url)

        if response.status_code in self.return_codes_ok:
            if 'results' in response.json().keys():
                audit_log = response.json()['results']
        else:
            audit_log = response.json()
        
        return audit_log


    def get_full_auditlog(self, **params):
        '''
        '''
        all_logs = []
        offset = 0
        limit = 1000

        audit_log = self.auditlog(_offset=str(offset), 
                                  _limit=str(limit), **params)
        while isinstance(audit_log, list) and len(audit_log):
            all_logs += audit_log
            offset += limit + 1
            audit_log = self.auditlog(_offset=str(offset), 
                                      _limit=str(limit), **params)

        return all_logs
    
    # Methods for undocumented API Calls - use at own risk

    def get_current_user(self, **params):
        '''
        Get Current User Data

        Parameters:
            **params (dict): Generic API parameters
        
        Returns:
            response object: Requests response object
        '''
        # Build URL
        url = self.base_url + '/v2/current_user'
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apiget(url)

        return response


    def get_users(self, **params):
        '''
        Get User Data

        Parameters:
            **params (dict): Generic API parameters
        
        Returns:
            response object: Requests response object
        '''
        # Build URL
        url = self.base_url + '/v2/users'
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apiget(url)

        return response


    def audit_users(self, domains=[]):
        '''
        Audit User Data for non compliant email domains

        Parameters:
            domain (list): List of valid email domains

        Returns:
            List of User Data (json)
        '''
        users = []
        user_data = []
        valid = False

        # Check for list of domains, otherwise use current users
        if len(domains) == 0:
            current_user = self.get_current_user().json()
            email = current_user['result']['email']
            domain = email.split('@')[1]
            domains.append(domain)
        logging.debug(f'Checking against domains: {domains}')

        # Get user data and check against valid domains
        response = self.get_users()
        user_data = response.json()['results']
        for user in user_data:
            valid = False
            for domain in domains:
                if domain in user['email']:
                    valid = True
                    break
            if not valid:
                users.append(user)
        
        return users
