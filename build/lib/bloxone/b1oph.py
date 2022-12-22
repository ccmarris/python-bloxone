#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 Module to provide class hierachy to simplify access to the BloxOne APIs

 Date Last Updated: 20221019

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
import bloxone
import logging
import json

# ** Global Vars **
__version__ = '0.2.3'
__author__ = 'Chris Marrison'
__email__ = 'chris@infoblox.com'
__doc__ = 'https://python-bloxone.readthedocs.io/en/latest/'
__license__ = 'BSD'


class b1oph(bloxone.b1):
    '''
    Class to simplify access to the BloxOne Platform APIs
    '''

    def __init__(self, cfg_file='config.ini'):
        '''
        Call base __init__ and extend
        '''
        super().__init__(cfg_file)

        self.OPH_COMPOSITE_STATUS = { '0': 'Review Details', 
                                      '1': 'Online',
                                      '2': 'Unknown',
                                      '3': 'Pending',
                                      '4': 'Awaiting approval' }
        
        self.OPH_PLATFORM_STATES = { '0': 'Offline',
                                     '1': 'Online',
                                     '2': 'Error',
                                     '3': 'Waiting (pending)',
                                     '4': 'Unknown' }
        
        self.OPH_HOST_TYPES = { '0': 'Not Available',
                                '1': 'Unknown',
                                '2': 'Unknown',
                                '3': 'BloxOne VM',
                                '4': 'BloxOne Appliance - B105',
                                '5': 'BloxOne Container',
                                '6': 'CNIOS' }
        
        self.OPH_APP_MGT = { '0': 'Inactive',
                             '1': 'Active',
                             '2': 'Error',
                             '3': '' }

        self.OPH_APPS = { '1': { 'AppName': 'DFP', 'StatusSpace': '9' },
                          '2': { 'AppName': 'DNS', 'StatusSpace': '12' },
                          '3': { 'AppName': 'DHCP', 'StatusSpace': '15' },
                          '7': { 'AppName': 'CDC', 'StatusSpace': '24' },
                          '9': { 'AppName': 'Anycast', 'StatusSpace': '30' },
                          '10': { 'AppName': 'NGC', 'StatusSpace': '34' },
                          '12': { 'AppName': 'MS AD Collector', 'StatusSpace': '40' },
                          '14': { 'AppName': 'Edge_Services_FW', 'StatusSpace': '46' },
                          '15': { 'AppName': 'Edge_Services_Router', 'StatusSpace': '49' },
                          '16': { 'AppName': 'Site-to-Site_VPN', 'StatusSpace': '52' },
                          '18': { 'AppName': 'DNS_Assured_Forwarding', 'StatusSpace': '58' },
                          '20': { 'AppName': 'NTP', 'StatusSpace': '64' }
        }

        self.OPH_APP_NAMES = { 'DFP': '1',
                               'DNS': '2',
                               'DHCP': '3',
                               'CDC': '7',
                               'Anycast': '9',
                               'NGC': '10' }

        self.APP_STATUS = { '0': 'inactive', '1': 'active', '2': 'stopped' }

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
            response object: Requests response object
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
            response object: Requests response object
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
            response object: Requests response object
        '''
        # Build url
        url = self.host_url + objpath
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apiput(url, body)

        return response


    def patch(self, objpath, id="", body=""):
        '''
        Generic create object wrapper for ddi objects

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.host_url + objpath
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apipatch(url, body)

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
            response object: Requests response object
        '''

        # Call BloxOne API
        response = self.get('/on_prem_hosts', **params)

        # Return response object
        return response 


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
            # Look for results or result
            if "results" in obj.keys():
                result_text = "results"
            elif "result" in obj.keys():
                result_text = "result"
            else:
                result_text = ""
            
            # Get result if available
            if result_text:
                obj = obj[result_text]
                if obj:
                    id = obj[0]['id']
                    if not include_path and "/" in str(id):
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


    def get_ophid(self, name=""):
        '''
        Return the ophid of named OPH

        Parameters:
            name (str): display name of OPH
        
        Returns:
            ophid(str): ophid of the specified OPH
        '''
        filter = f'display_name=="{name}"'
        response = self.get('/on_prem_hosts', _filter=filter, _fields="display_name,ophid")
        if response.status_code in self.return_codes_ok:
            if 'result' in response.json().keys():
                ophid = response.json()['result'][0]['ophid']
            else:
                ophid = ''
        else:
            ophid = ''

        return ophid


    def oph_add_tag(self, id="", tagname="", tagvalue=""):
        '''
        Method to add a tag to an existing On Prem Host

        Parameters:
            objpath (str):  Swagger object path
            tagname (str): Name of tag to add
            tagvalue (str): Value to associate

        Returns:
            response object: Requests response object
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
            response object: Requests response object
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


    def oph_status_summary(self, name="", id="", tags=False):
        '''
        Get OPH status information for one or more OPHs

        Parameters:
            name (ste): Display name of OPH
            id (str): id of a specific OPH
            tags (bool): include tags in report
        
        Returns:
            rpt: Dict of translated status elements
        '''
        rpt = None

        # Get OPH Data
        if name:
            name_filter = 'display_name=="' + name + '"'
            response = self.get('/on_prem_hosts', _filter=name_filter)
        elif id:
            response = self.get('/on_prem_hosts', id=id)
        else:
            response = self.get('/on_prem_hosts')
        
        if response.status_code in self.return_codes_ok:
            rpt = self.oph_status_rpt(response.json(), tags=tags)
        else:
            logging.error(f'Response code: {response.status_code}, Data: {response.text}')
            rpt = None
    
        return rpt


    def oph_status(self, oph_data):
        '''
        Translate status info in JSON data for an OPH

        Parameters:
            oph_data (dict): Data for individual OPH
        
        Returns:
            oph_status: Dict of translated status elements
        '''
        oph_status = {}
        oph_comp_state = ''
        oph_plat_state = ''
        oph_plat_msg = ''
        oph_app_mgt = ''
        oph_app_msg = ''

        if 'composite_status' in oph_data.keys():
            oph_comp_state = self.OPH_COMPOSITE_STATUS[oph_data['composite_status'].get('status')]
        else:
            oph_comp_state = 'No state information'
                        
        if 'state' in oph_data.keys():
            if oph_data['state'].get('current_state') in self.OPH_PLATFORM_STATES.keys():
                oph_plat_state = self.OPH_PLATFORM_STATES[oph_data['state'].get('current_state')]
            else:
                oph_plat_state = f"Unknown state: {oph_data['state'].get('current_state')}"

            if 'message' in oph_data['state'].keys():
                oph_plat_state = oph_data['state']['message']

        else:
            oph_plat_state = "Platform status unavailable"
        
        if 'status' in oph_data.keys():
            oph_app_mgt = self.OPH_PLATFORM_STATES[oph_data['status'].get('status')]
            if 'message' in oph_data['status'].keys():
                oph_app_msg = oph_data['status']['message']
        else:
            oph_app_mgt = "Application Management status unavailable"

        oph_status = { 'OPH State': oph_comp_state,
                       'Platform Management': oph_plat_state,
                       'Application Management': oph_app_mgt }
        
        if oph_plat_msg:
            oph_status.update( {'Platform Message': oph_plat_msg })
        if oph_app_msg:
            oph_status.update( {'App Mgt Message': oph_app_msg })
        
        return oph_status
    

    def oph_app_status(self, oph_data):
        '''
        Translate App status info in JSON data for an OPH

        Parameters:
            oph_data (dict): Data for individual OPH
        
        Returns:
            oph_apps: Dict of translated status elements
        '''
        oph_apps = {}
        app_id = ''
        app_name = ''
        ver_name = ''
        status = ''
        app_version = None

        # Check for application status data
        if 'applications' in oph_data.keys():
            for app in oph_data['applications']:
                app_id = app.get('application_type')
                if app_id in self.OPH_APPS.keys():
                    app_name = self.OPH_APPS[app_id]['AppName']
                    ver_name = app_name + '_version'
                else:
                    app_name = 'Unknown, AppID: ' + app_id

                # Check whether app is enabled
                status = self.APP_STATUS[app['composite_status']['status']]
                if app.get('disabled') == '1':
                    status = f'disabled - {status}'

                app_version = app.get('current_version')

                # Add version info if available
                if app_version:
                    oph_apps.update( { app_name: status,
                                        ver_name: app_version } )
                else:
                    oph_apps.update( { app_name: status } )

        else:
            oph_apps = {}
        
        return oph_apps
   

    def oph_status_rpt(self, json_data, tags=False):
        '''
        Build  status report from GET /on_prem_hosts data

        Parameters:
            json_data (json): API JSON data for On Prem Hosts call
            tags (bool): Include tags in response, default False
        
        Returns:
            rpt: Dict of status elements
        '''
        rpt = {}
        on_prem_host = ""
        oph_status = {}
        oph_apps = {}

        if json_data:
            results = json_data.get('result')
            if not isinstance(results, list):
                results = [ results ]
            # Build report 
            for oph in results:
                oph_apps = {}
                on_prem_host = oph.get('display_name')
                if on_prem_host:
                    oph_status = self.oph_status(oph)
                    oph_apps = self.oph_app_status(oph)

                    rpt.update( { on_prem_host: { 'status': oph_status,
                                          'id': oph.get('id'),
                                          'host_type': self.OPH_HOST_TYPES[oph.get('host_type')],
                                          'ip_address': oph.get('ip_address'), 
                                          'nat_ip': oph.get('nat_ip'),
                                          'version': oph.get('current_version'),
                                          'last_seen': oph.get('last_seen'),
                                          'applications': oph_apps }
                                } )
                if tags:
                    rpt[on_prem_host].update({'tags': oph.get('tags')})
        else:
            rpt = None

        return rpt

    
    def oph_uptime(self, name=""):
        '''
        '''
        uptime = None
        ophid = self.get_ophid(name=name)
        url = 'https://csp.infoblox.com/atlas-status-service/v1/getsummary'
        body = '{"objectID":["' + ophid +'"],"objectType":["Onprem Host ID"],"event_key":["health-collector/heartbeat/"]}'
        response = self._apipost(url, body=body)
        if response.status_code in self.return_codes_ok:
            uptime = response.json()['results'][0]['metadata']['hostUptime']
        
        return uptime


    def get_app_state(self, name, app):
        '''
        Get status of application for an OPH

        Parameters:
            name (str): display_name of OPH
            app (str): App Name, e.g. DNS
        
        Returns:
            app_status (str): Status or error msg as text
        '''
        status_data = ''
        app_status = ''

        status_data = self.oph_status_summary(name=name)
        if status_data:
            if 'applications' in status_data[name].keys():
                app_status = status_data[name]['applications'].get(app)
                if not app_status:
                    logging.error(f'App: {app} not found for OPH: {name}')
                    app_status = f'App: {app} not found for OPH: {name}'
            else:
                logging.error(f'No application data for OPH: {name}')
                app_status = f'No application data for OPH: {name}'

        else:
            logging.error(f'OPH: {name} not found')
            app_status = f'OPH: {name} not found'

        return app_status


    def manage_app(self, name="", app="", action="status"):
        '''
        Perform action on named OPH for specified app

        Parameters:
            name (str): display_name of OPH
            app (str): App Name, e.g. DNS
            action (str): action to perform for app
        
        Returns:
            bool
        '''
        result = False
        actions = [ 'status', 'disable', 'enable', 'stop', 'start' ]

        if action in actions:
           if action == "status":
               result = self.get_app_state(name=name, app=app) 
           elif action == "disable":
               result = self.disable_app(name=name, app=app) 
           elif action == "enable":
               result = self.enable_app(name=name, app=app) 
           elif action == "start":
               result = self.app_process_control(name=name, 
                                                 app=app, 
                                                 action="start") 
           elif action == "stop":
               result = self.app_process_control(name=name, 
                                                 app=app, 
                                                 action="stop") 
           else:
               logging.error(f'Action: {action} not implemented')
               result = False
        else:
            logging.error(f'Action: {action} not supported')
            logging.info(f'Supported actions: {actions}')
            result = False

        return result


    def disable_app(self, name="", app=""):
        '''
        Disable specified app on named OPH

        Parameters:
            name (str): display_name of OPH
            app (str): App Name, e.g. DNS
        
        Returns:
            bool
        '''
        status = False
        app_type = ''

        # Check app supported and get Get application_type
        if app in self.OPH_APP_NAMES.keys():
            app_type = self.OPH_APP_NAMES[app]
        elif app in self.OPH_APPS.keys():
            app_type = app

        if app_type:
            # Get id of OPH
            filter = f'display_name=="{name}"'
            response = self.get('/on_prem_hosts', 
                                _filter=filter)
            if response.status_code in self.return_codes_ok:
                oph_data = response.json()['result']
                id = oph_data[0]['id']
                logging.debug(f'On Prem Host id = {id}')

                # Build body
                body = { 'display_name': name, 
                         'applications': [ { 'application_type': app_type,
                                             'disabled': '1', 
                                             'state': { 'desired_state': '0' } 
                                           } ] } 
                
                # Update desired OPH
                response = self.update('/on_prem_hosts',
                                       id=id,
                                       body=json.dumps(body))
                if response.status_code in self.return_codes_ok:
                    logging.debug(f'OPH: {name}, App: {app}, App_type: {app_type}')
                    status = True
                else:
                    logging.error(f'{response.status_code}: {response.text}')

            else:
                logging.error(f'OPH {name} not found.')
                status = False
        else:
            logging.error(f'App {app} not supported.')
            status = False
        
        return status


    def enable_app(self, name="", app=""):
        '''
        Enable specified app on named OPH

        Parameters:
            name (str): display_name of OPH
            app (str): App Name, e.g. DNS
        
        Returns:
            bool
        '''
        status = False
        app_type = ''

        # Check app supported and get Get application_type
        if app in self.OPH_APP_NAMES.keys():
            app_type = self.OPH_APP_NAMES[app]
        elif app in self.OPH_APPS.keys():
            app_type = app

        if app_type:
            # Get id of OPH
            filter = f'display_name=="{name}"'
            response = self.get('/on_prem_hosts', 
                                _filter=filter)
            if response.status_code in self.return_codes_ok:
                oph_data = response.json()['result']
                id = oph_data[0]['id']
                logging.debug(f'On Prem Host id = {id}')

                # Build body
                body = { 'display_name': name, 
                         'applications': [ { 'application_type': app_type,
                                             'disabled': '0', 
                                             'state': { 'desired_state': '1' } 
                                           } ] } 
                
                # Update desired OPH
                response = self.update('/on_prem_hosts',
                                       id=id,
                                       body=json.dumps(body))
                if response.status_code in self.return_codes_ok:
                    logging.debug(f'OPH: {name}, App: {app}, App_type: {app_type}')
                    status = True
                else:
                    logging.error(f'{response.status_code}: {response.text}')

            else:
                logging.error(f'OPH {name} not found.')
                status = False
        else:
            logging.error(f'App {app} not supported.')
            status = False
        
        return status
    

    def app_process_control(self, name="", app="", action=""): 
        '''
        Start or stop an application process

        Parameters:
            name (str): display_name of OPH
            app (str): App Name, e.g. DNS
        
        Returns:
            bool 
        '''
        app_type = ''
        status = False
        actions = { "start": '1', "stop": '0' }

        if action in actions.keys():

            # Check app supported and get Get application_type
            if app in self.OPH_APP_NAMES.keys():
                app_type = self.OPH_APP_NAMES[app]
            elif app in self.OPH_APPS.keys():
                app_type = app

            if app_type:
                # Get id of OPH
                oph_status = self.oph_status_summary(name=name)
                if oph_status:
                    id = oph_status.get('id')
                    logging.debug(f'On Prem Host id = {id}')
                    app_status = oph_status[name]['applications'].get(app)
                    logging.debug(f'App status: {app} app is {app_status}')
                    # Check whether app is disabled
                    if 'disabled' not in app_status:
                        # Build body
                        body = { 'display_name': name, 
                                'applications': [ { 'application_type': app_type,
                                                    'disabled': '0', 
                                                    'state': 
                                                        { 'desired_state': actions[action] } 
                                                } ] } 
                        
                        # Update desired OPH
                        response = self.update('/on_prem_hosts',
                                            id=id,
                                            body=json.dumps(body))
                        if response.status_code in self.return_codes_ok:
                            logging.debug(f'OPH: {name}, App: {app}, App_type: {app_type}')
                            status = True
                        else:
                            logging.error(f'{response.status_code}: {response.text}')
                            status = False
                    else:
                        logging.info(f'App: {app} on OPH: {name} {app_status}')
                        status = False

                else:
                    logging.error(f'OPH {name} not found.')
                    status = False
            else:
                logging.error(f'App {app} not supported.')
                status = False
        else:
            logging.error(f'Action: {action} not supported')
            status = False

        return status
