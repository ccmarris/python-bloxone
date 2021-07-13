#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 Module to provide class hierachy to simplify access to the BloxOne APIs

 Date Last Updated: 20210713

 Todo:

 Copyright (c) 2021 Chris Marrison / Infoblox

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
from bloxone.b1oph import b1oph
import bloxone
import logging
import requests
import json

# ** Global Vars **
__version__ = '0.1.0'
__author__ = 'Chris Marrison'
__email__ = 'chris@infoblox.com'
__doc__ = 'https://python-bloxone.readthedocs.io/en/latest/'
__license__ = 'BSD'


class APIError_Unable_To_Retrieve_Commands(Exception):
    '''
    Exception for API call in __init__
    '''
    pass


class Command_Not_Supported(Exception):
    '''
    Exception for API call in __init__
    '''
    pass


class Unknown_Argument(Exception):
    '''
    Exception for API call in __init__
    '''
    pass


class b1diagnostics(bloxone.b1):
    '''
    Class to simplify access to the BloxOne Platform APIs
    '''

    def __init__(self, cfg_file='config.ini'):
        '''
        Call base __init__ and extend
        '''
        super().__init__(cfg_file)

        # Instantiate b1oph class as need access to b1oph.get_ophid()
        self.b1_oph = b1oph(cfg_file)

        # Automatically get list of remote_commands
        try:
            response = self.get_remote_commands()
            self.commands = response.json()['results']
        except:
            logging.error(f'Response code: {response.status_code}')
            logging.error(f'Response body: {response.text}')
            raise APIError_Unable_To_Retrieve_Commands()
        
        return


    def get(self, objpath, id="", action="", **params):
        '''
        Generic get object wrapper for platform calls

        Parameters:
            objpath (str):  Swagger object path
            id (str):       Optional Object ID
            action (str):   Optional object action, e.g. "nextavailableip"

        Returns:
            response object: Requests response object
        '''

        # Build url
        url = self.diagnostics_url + objpath
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        response = self._apiget(url)

        return response

        
    def post(self, objpath, body=""):
        '''
        Generic create object wrapper for platform objects

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.diagnostics_url + objpath
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
            response object: Requests response object
        '''
        # Build url
        url = self.diagnostics_url + objpath
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
            response object: Requests response object
        '''
        # Build url
        url = self.diagnostics_url + objpath
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apiput(url, body)

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

    # Helper Methods

    '''
    def get_ophid(self):
        return ophid
    '''

    def get_remote_commands(self):
        '''
        Get set of possible remote commands and parameters

        Returns:
            response object: Requests response object
        '''
        return self.get('/remotecommands')


    def is_command(self, command):
        '''
        Check whether command is valid

        Parameters:
            command(str): command to check
        
        Returns:
            boolean
        '''
        cmds = []
        for cmd in self.commands:
            cmds.append(cmd['name'])
        if command in cmds:
            status = True
        else:
            status = False
        return status

    
    def get_args(self, command):
        '''
        Check the args for a command

        Parameters:
            command(str): Command to retrieve argyments for

        Returns:
            Disctionary of arguments or empty dictionary if none.
        
        Raises:
            Command_Not_Supported Exception if command is not available
        '''
        args = {}
        if self.is_command(command):
            for cmd in self.commands:
                if cmd['name'] == command:
                    if 'args' in cmd.keys():
                        args = cmd['args']
                    else:
                        args = {}
                    break
        else:
            raise Command_Not_Supported(f'Command: {command} not supported.')
        
        return args



    def execute_task(self, command, args={}, ophname=None, 
                     ophid=None, id_only=True, priv=False):
        '''
        Execute remote command on an OPH
    
        Parameters:
            cmd(str): Command to execute
            args(dict): Command arguments
            ophname(str): Name of OPH to execute command on (or supply ophid)
            ophid(str): (Optional) ophid of OPH for cmd execution
            id_only(bool): default of True
            priv(bool): Run privileged task, default of False

        Returns:
            id string of task if id_only=True (defult)
            response object: Requests response object if id_only=False

        Raises:
            TypeError Exception if required options not supplied 
            KeyErro Exception if ophname is not found (and ophid not supplied)
            Command_Not_Supported Exception if command is not valid
            Unknown_Argument Exception if arguments do not match required
        
        Todo:
            [ ] Enhance logic to run /priviledgetask or /task
            Awaiting API enhancement to determine priv versus non-priv
            [ ] Enhance args check for required arguments
            Awaiting API enhancement for arg to determine required versus 
            optional arguments
        '''
        # Check command is valid
        if self.is_command(command):
            # If ophid supplied then get this
            if ophid or ophname: 
                if not ophid:
                    logging.debug(f'Getting ophid for OPH: {ophname}')
                    ophid = self.b1_oph.get_ophid(name=ophname)
                    if not ophid:
                        logging.error(f'OPH not found.')
                        raise KeyError(f'OPH {ophname} not found')
                logging.debug(f'OPHID: {ophid}')

                # Check args
                arglist = self.get_args(command)
                for arg in args.keys():
                    if arg not in arglist.keys():
                        raise Unknown_Argument(f'Argument: {arg} not recognised')
                    s_type = type(args[arg]) 
                    ex_type = type(arglist[arg])
                    if s_type != ex_type:
                        raise TypeError(f'Supplied argument type {s_type}' +
                            f' does not match expected type {ex_type}')

                # Create command body
                body = '{ "cmd": '
                if len(args) > 0:
                    body = body + '{ "args": ' + json.dumps(args) + ', '
                else:
                    body = body + '{ '
                body = body + '"name": "' + command + '" }, '
                body = body + '"ophid": "' + ophid + '" }'
                logging.debug(f'Task body: {body}')

                # Execute
                if priv:
                    response = self.post('/privilegedtask', body=body)
                else:
                    response = self.post('/task', body=body)
                if id_only:
                    if response.status_code in self.return_codes_ok:
                        id = response.json()['result']['id']
                    else:
                        error_msg = ( 'Failed to create task, ' +
                                    f'HTTP Code: {response.status_code}')
                        logging.error(error_msg)
                        id = None
                    result = id
                else:
                    result = response

            else:
                logging.error('No ophname or ophid supplied.')
                raise TypeError('Requires either ophname or ophid to be defined')
        else:
            logging.error(f'Command: {command} is not a supported command')
            raise Command_Not_Supported(f'Command: {command} not supported.')
        
        return result


    def get_task_result(self, taskid):
        '''
        Get the results for specidied task

        Parameters:
            taskid(str): id of executed task
        
        Returns:
            response object: Requests response object if id_only=False
        '''
        id = '/task/' + taskid
        return self.get(id)
        

    def download_task_results(self, taskid):
        '''
        Get the results for specidied task

        Parameters:
            taskid(str): id of executed task
        
        Returns:
            response object: Requests response object if id_only=False

        Note:

        '''
        id = '/task/' + taskid + '/download'
        return self.get(id)
        