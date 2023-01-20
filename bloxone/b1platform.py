#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 Module to provide class hierachy to simplify access to the BloxOne APIs

 Date Last Updated: 20230119

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
__version__ = '0.8.2'
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


    def get_current_user_accounts(self, **params):
        '''
        Get Current Users Accounts Data

        Parameters:
            **params (dict): Generic API parameters
        
        Returns:
            response object: Requests response object
        '''
        # Build URL
        url = self.base_url + '/v2/current_user/accounts'
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apiget(url)

        return response


    def get_current_tenant(self, **params):
        '''
        Get name of current tenant

        Parameters:
            **params (dict): Generic API parameters
        
        Returns:
            string containing name of tenant or '' on failure
        '''
        tenant_name = ''

        current_user = self.get_current_user()
        if current_user.status_code in self.return_codes_ok:
            user_id = current_user.json()['result']['account_id']
            user_accounts = self.get_current_user_accounts()
            for account in user_accounts.json()['results']:
                if user_id == account['id']:
                    tenant_name = account['name']
                    break
        else:
            logging.error('Failed to get account details API reponded with')
            logging.error(f'HTTP code: {current_user.status_code} ')
            logging.error(f'Response: {current_user.text}')
            tenant_name = ''
        
        return tenant_name

    
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
    

    def get_user_id(self, email="", include_path=False):
        '''
        Get object id using key/value pair

        Parameters:
            email (str):    email address of user account
            include_path (bool): Include path to object id

        Returns:
            id (str):   object id or ""
        '''

        # Local Variables
        id = ""

        # Make API Call
        response = self.get_users()

        # Process response
        if response.status_code in self.return_codes_ok:
            users = response.json().get('results')
            if users:
                for user in users:
                    if email == user.get('email'):
                        id = user.get('id')
                        if not include_path:
                            id = id.rsplit('/',1)[1]
                        break 
                else:
                    logging.debug("User account {} not found."
                                  .format(email))
            else:
                id = ""
                logging.debug("No results found.")
        else:
            id=""
            logging.debug("HTTP Error occured. {}".format(response.status_code))

        logging.debug("id: {}".format(id)) 

        return id


    def create_user(self, name='', 
                          email='', 
                          type='interactive',
                          authenticator='IDP',
                          groups=['user', 'act_admin'],
                          **params):
        '''
        Create User Account

        Parameters:
            **params (dict): Generic API parameters
        
        Returns:
            response object: Requests response object
        '''
        # Build URL
        url = self.base_url + '/v2/users'
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        groups = self.get_group_ids(groups=groups)

        body = { 'name': name,
                 'email': email,
                 'type': type,
                 'authenticator': authenticator,
                 'groups': groups 
               }

        # Make API Call
        response = self._apipost(url, body=json.dumps(body))

        return response


    def delete_user(self, email='', **params):
        '''
        Create User Account

        Parameters:
            **params (dict): Generic API parameters
        
        Returns:
            response object: Requests response object
        '''
        # Build URL
        url = self.base_url + '/v2/users'
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        user_id = self.get_id(url, key='email', 
                              value=email, 
                              include_path=False)
        
        logging.debug("ID: {}".format(user_id))

        if user_id:
            url = url + '/' + user_id
            # Make API Call
            response = self.delete(url)

        else:
            response = self._not_found_response

        return response


    def get_groups(self, **params):
        '''
        Get User Groups

        Parameters:
            **params (dict): Generic API parameters
        
        Returns:
            response object: Requests response object
        '''
        # Build URL
        url = self.base_url + '/v2/groups'
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apiget(url)

        return response


    def get_group_ids(self, groups=['user'], **params):
        '''
        Get User Group IDs

        Parameters:
            groups (list): List of group names
            **params (dict): Generic API parameters
        
        Returns:
            response object: Requests response object
        '''
        group_ids = []
        
        # Make API Call
        response = self.get_groups(_fields='name,id')
        if response.status_code in self.return_codes_ok:
            grps = response.json().get('results') 
            group_ids = [ grps[x].get('id') for x in range(len(grps)) 
                            if grps[x].get('name') in groups ]
            '''
            for grp in grps:
                if grp.get('name') in groups:
                    group_ids.append(grp.get('id'))
                    logging.debug(f'Found id for group {grp.get("name")}')
            '''
        else:
            logging.error('Failed to get User Groups API reponded with')
            logging.error(f'HTTP code: {response.status_code} ')
            logging.error(f'Response: {response.text}')
            group_ids = []

        return group_ids
    

    def global_search_version(self):
        '''
        Get the global search version information

        Returns:
            response object: Requests response object

        '''
        url = f'{self.base_url}/atlas-search-api/v1/version'
        return self.get(url)


    def global_search(self, query='', limit=None, filters=[], offset=0, **params):
        '''
        Perform a global search

        Parameters:
            query (str): Search term
            limit (int): Max number of records to match
            filters (list): list of filter definitions
            offset (int): record offset
            **params: Additional parameters
        
        Returns:
            response object: Requests response object

        '''
        body = {}
        url = f'{self.base_url}/atlas-search-api/v1/search'
        body['query'] = query
        body['filters'] = filters
        if limit:
            body['limit'] = limit
        if offset > 0:
            body['offset'] = offset
        if params:
            body.update(params)
        
        return self.post(url, body=json.dumps(body))


    def simple_global_search(self, query=''):
        '''
        Simple form of global_search() returning list of objects with ids

        Parameters:
            query (str): Search term
        
        Returns:
            result (list): List of dict of object ids and metadata
                           [ { '_id': id, 'metadata': dict of metadata } ]

        '''
        result = []
        response = self.global_search(query=query)
        if response.status_code in self.return_codes_ok:
            hits = response.json()['hits']['hits']
            if hits:
                for obj in hits:
                    result.append({ '_id': obj.get('_id'),
                                    'name': obj.get('_source').get('doc').get('name'),
                                    'summary': obj.get('_source').get('doc').get('summary'),
                                    'metadata': obj.get('_source').get('metadata') })
            else:
                result = []
        else:
            logging.error('Global Search Failed')
            logging.error(f'HTTP code: {response.status_code} ')
            logging.error(f'Response: {response.text}')

        return result