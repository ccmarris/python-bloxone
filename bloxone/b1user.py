#!/usr/bin/env python3
#vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''

 Description:

    BloxOne b1user class providing an simple data interface for user info 

 Requirements:
   Python3 with re, ipaddress, requests and sqlite3 modules

 Author: Chris Marrison

 Date Last Updated: 20230127

 Todo:

 Copyright (c) 2023 Chris Marrison / Infoblox

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

'''
__version__ = '0.1.0'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import bloxone
import logging


class b1user(bloxone.b1platform):
    '''
    '''
    def __init__(self,
                 username: str = '', 
                 email_domain: str = 'infoblox.com',
                 b1org: str = '', 
                 delete: bool = False, 
                 cfg_file='config.ini'):
        '''
        Initialise class

        Parameters:
            username (str): Username or email address
            email_domain (str): email domain of user
            b1org (str): Name of org 
            delete (bool): Delete data and user or report only
            cfgfile (str): inifile to user for bloxone module
        '''
        super().__init__(cfg_file)

        self.username = username
        self.email_domain = email_domain
        self.b1org = b1org
        self.delete = delete
        
        user_dict = self.convert_username()
        self.owner = user_dict.get('owner')
        self.email = user_dict.get('email')

        self.current_org = self.get_current_tenant()

        return


    def convert_username(self) -> dict:
        '''
        '''
        user_dict = {}
        u = self.username.casefold()
        if '@' in self.username:
            user = u.split('@')[0]
            email = self.username
        else:
            user = u
            email = f'{u}@{self.email_domain}'
        
        user_dict = { 'owner': user, 'email': email }

        return user_dict


    def check_tenant(self) -> bool:
        '''
        Check Org
        '''
        return self.current_org == self.b1org


    def user_exists(self) -> bool:
        '''
        '''
        status = False
        user_id = self.get_user_id(self.email)
        if user_id:
            status = True
        else:
            status = False

        return status


    def is_current_user(self) -> bool:
        '''
        '''
        status = False
        response = self.get_current_user()
        if response.status_code in self.return_codes_ok:
            current_user = response.json().get('result').get('email')
            if self.email == current_user:
                status = True
            else:
                status = False
        else:
            logging.error('Could not determine current user.')
            logging.error(f'HTTP code: {response.status_code} ')
            logging.error(f'Response: {response.text}')
            raise

        return status

        
    def find_user_objects(self) -> dict:
        '''
        '''
        return self.simple_global_search(self.owner)


    def find_join_tokens(self) -> dict:
        '''
        '''
        filter = f'name~"{self.username}*."'
        response = self.get_join_token(_filter=filter)
        if response.status_code in self.return_codes_ok:
            result = response.json().get('results')
        else:
            logging.error(f'HTTP code: {response.status_code} ')
            logging.error(f'Response: {response.text}')
            result = {}

        return result


    def find_ophs(self) -> dict:
        '''
        '''
        filter = f'display_name~"{self.owner}*."'
        response = self.on_prem_hosts(_filter=filter)
        if response.status_code in self.return_codes_ok:
            result = response.json().get('result')
        else:
            logging.error(f'HTTP code: {response.status_code} ')
            logging.error(f'Response: {response.text}')
            result = {}

        return result


    def data_report(self) -> bool:
        '''
        '''
        status = False
        lines = []
        search = self.find_user_objects()
        jts = self.find_join_tokens()
        ophs = self.find_ophs()

        if search or jts or ophs:
            # We found something
            status = True
            if search:
                print('Data objects:\n')
                for item in search:
                    lines.append( f'Name: {item.get("name")}, ' +
                                  f'Resource: {item.get("metadata").get("resource")}, ' +
                                  f'Tags: {item.get("tags")}' )
                for l in lines:
                    print(l)
            else:
                print('No data objects found.')

            if jts:
                lines = []
                for item in jts:
                    lines.append( f'Name: {item.get("name")}, ' +
                                  f'Status: {item.get("status")}, ' +
                                  f'Use-counter: {item.get("use_counter")}' +
                                  f'Tags: {item.get("tags")}' )
                # Print results
                print('\nJoin Tokens:\n')
                for l in lines:
                    print(l)
            else:
                print('No join tokens found.')
            
            if ophs:
                lines = []
                for item in ophs:
                    lines.append( f'Name: {item.get("display_name")}, ' +
                                  f'Last seen: {item.get("last_seen")}, ' +
                                  f'Tags: {item.get("tags")}' )
                # Print results
                print('\nOn Prem Hosts:\n')
                for l in lines:
                    print(l)
            else:
                print('No OPHs found.')

        else:
            # Nothing found
            status = False

        return status

"""
            # Check current user
            if delete:
                # Check current user
                response = b1p.get_current_user()
                if response.status_code in b1p.return_codes_ok:
                    current_user = response.json().get('email')
                    if current_user == user['email']:
                        logging.error('Attempting to delete current user!')
                        exitcode = 1
                        raise exit(exitcode)
                else:
                    logging.error('Could not determine current user.')
                    logging.error(f'Response code: {response.status_code}')
                    logging.error(f'Message: {response.text}')
                    exitcode = 2
                    raise exit(exitcode)
            
            # Collect

                
            '''
            Input: Username and Org
            - Check for correct Org
            - Determine username
                - Does user exist
            - Find objects
            - Process object list
                - Determine Objecname and Owner tags
                - Check against username
                - Report
            - Delete process
                - order of deletion
                - delete objects

            '''

        
        else:
            logging.error(f'Running against wrong BloxOne Org.')
            logging.info(f'Current Org: {org}')
            exitcode = 1

        return status
"""

### Main ###
if __name__ == '__main__':
    exit(1)
## End Main ###