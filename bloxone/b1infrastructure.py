#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 Module to provide class hierachy to simplify access to the BloxOne APIs

 Date Last Updated: 20230608

 Todo:

    Complete the service control methods

 Copyright (c) 2021-2023 Chris Marrison / Infoblox

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
__version__ = '0.0.6'
__author__ = 'Chris Marrison'
__email__ = 'chris@infoblox.com'
__doc__ = 'https://python-bloxone.readthedocs.io/en/latest/'
__license__ = 'BSD'


class b1infra(bloxone.b1):
    '''
    Class to simplify access to the BloxOne Platform APIs
    This class replaces the deprecated b1oph class
    '''

    def __init__(self, cfg_file='config.ini'):
        '''
        Call base __init__ and extend
        '''
        super().__init__(cfg_file)

        self.b1host_COMPOSITE_STATUS = { '0': 'Review Details', 
                                      '1': 'Online',
                                      '2': 'Unknown',
                                      '3': 'Pending',
                                      '4': 'Awaiting serviceroval' }
        
        self.b1host_PLATFORM_STATES = { '0': 'Offline',
                                     '1': 'Online',
                                     '2': 'Error',
                                     '3': 'Waiting (pending)',
                                     '4': 'Unknown' }
        
        self.b1host_HOST_TYPES = { '0': 'Not Available',
                                '1': 'Unknown',
                                '2': 'Unknown',
                                '3': 'BloxOne VM',
                                '4': 'BloxOne serviceliance - B105',
                                '5': 'BloxOne Container',
                                '6': 'CNIOS' }
        
        self.b1host_service_MGT = { '0': 'Inactive',
                             '1': 'Active',
                             '2': 'Error',
                             '3': '' }

        self.b1host_services = { '1': { 'serviceName': 'DFP', 'StatusSpace': '9' },
                          '2': { 'serviceName': 'DNS', 'StatusSpace': '12' },
                          '3': { 'serviceName': 'DHCP', 'StatusSpace': '15' },
                          '7': { 'serviceName': 'CDC', 'StatusSpace': '24' },
                          '9': { 'serviceName': 'Anycast', 'StatusSpace': '30' },
                          '10': { 'serviceName': 'NGC', 'StatusSpace': '34' },
                          '12': { 'serviceName': 'MS AD Collector', 'StatusSpace': '40' },
                          '13': { 'serviceName': 'Access Authentication', 'StatusSpace': '43' },
                          '14': { 'serviceName': 'Edge_Services_FW', 'StatusSpace': '46' },
                          '15': { 'serviceName': 'Edge_Services_Router', 'StatusSpace': '49' },
                          '16': { 'serviceName': 'Site-to-Site_VPN', 'StatusSpace': '52' },
                          '18': { 'serviceName': 'DNS_Assured_Forwarding', 'StatusSpace': '58' },
                          '20': { 'serviceName': 'NTP', 'StatusSpace': '64' }
        }

        self.b1host_service_NAMES = { 'DFP': '1',
                               'DNS': '2',
                               'DHCP': '3',
                               'CDC': '7',
                               'Anycast': '9',
                               'NGC': '10' }

        self.service_STATUS = { '0': 'inactive', '1': 'active', '2': 'stopped' }

        return


    def get(self, objpath, id="", action="", **params):
        '''
        Generic get object wrserviceer for platform calls

        Parameters:
            objpath (str):  Swagger object path
            id (str):       Optional Object ID
            action (str):   Optional object action, e.g. "nextavailableip"

        Returns:
            response object: Requests response object
        '''

        # Build url
        url = self.infra_url + objpath
        url = self._use_obj_id(url,id=id)
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        response = self._apiget(url)

        return response

        
    def create(self, objpath, body=""):
        '''
        Generic create object wrserviceer for platform objects

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.infra_url + objpath
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apipost(url, body)

        return response


    def delete(self, objpath, id=""):
        '''
        Generic delete object wrserviceer for platform objects

        Parameters:
            objpath (str):  Swagger object path
            id (str):       Object id to delete

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.infra_url + objpath
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apidelete(url)

        return response


    def update(self, objpath, id="", body=""):
        '''
        Generic create object wrserviceer for ddi objects

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.infra_url + objpath
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apiput(url, body)

        return response


    def patch(self, objpath, id="", body=""):
        '''
        Generic create object wrserviceer for ddi objects

        Parameters:
            objpath (str):  Swagger object path
            body (str):     JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.infra_url + objpath
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
            logging.debug(f'HTTP Error occured. {response.status_code}')
            logging.debug(f'Body: {response.content}')
            tags = {}
        
        return tags


    # *** B1 Host/Service API Requests *** 

    def b1_hosts(self, **params):
        '''
        Method to retrieve BloxOne Hosts

        Parameters:
            **params (dict): Generic API parameters

        Returns:
            response object: Requests response object
        '''

        # Call BloxOne API
        response = self.get('/hosts', **params)

        # Return response object
        return response 


    def b1_detail_hosts(self, **params):
        '''
        Method to retrieve BloxOne Hosts
        Note: Undocumented and subject to change

        Parameters:
            **params (dict): Generic API parameters

        Returns:
            response object: Requests response object
        '''

        # Call BloxOne API
        response = self.get('/detail_hosts', **params)

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


    def get_ophid(self, objpath, *, key="", value="", include_path=False):
        '''
        Get object id using key/value pair

        Parameters:
            objpath (str):  Swagger object path
            key (str):      name of key to match
            value (str):    value to match
            include_path (bool): Include path to object id

        Returns:
            id (str):       ophid or ""
        '''

        # Local Variables
        id = ""
        filter = key+'=="'+value+'"'
        fields = key + ',ophid'

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
                    id = obj[0]['ophid']
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


    def get_b1host_id(self, name="", ophid=False):
        '''
        Return the id of named BloxOne Host

        Parameters:
            name (str): display name of b1host
        
        Returns:
            b1hostid(str): b1hostid of the specified b1host
        '''
        if ophid:
            id = self.get_ophid('/hosts', key="display_name", value=name, include_path=False)
        else:
            id = self.get_id('/hosts', key="display_name", value=name, include_path=False)
        
        return id


    def b1host_add_tag(self, id="", tagname="", tagvalue=""):
        '''
        Method to add a tag to an existing B1 Host

        Parameters:
            objpath (str):  Swagger object path
            tagname (str): Name of tag to add
            tagvalue (str): Value to associate

        Returns:
            response object: Requests response object
        '''
        # tags = self.get_tags('/hosts', id=id)
        response = self.get('/hosts', id=id, _fields="display_name,tags")
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
        response = self.update('/hosts', id=id, body=json.dumps(data))

        return response


    def b1host_delete_tag(self, id="", tagname=""):
        '''
        Method to delete a tag from an existing B1 Host

        Parameters:
            objpath (str):  Swagger object path
            tagname (str): Name of tag to add

        Returns:
            response object: Requests response object
        '''
        # tags = self.get_tags('/hosts', id=id)
        response = self.get('/hosts', id=id, _fields="display_name,tags")
        if response.status_code in self.return_codes_ok:
            data = response.json()['result']
            logging.debug("Existing tags: {}".format(data))
            # Delete tag from data
            if tagname in data['tags'].keys():
                data['tags'].pop(tagname, True)
                print(json.dumps(data))
                logging.debug("New tags: {}".format(data))
                # Update object
                response = self.update('/hosts', id=id, body=json.dumps(data))
        else:
            logging.debug(f'HTTP Error occured. {response.status_code}')
            logging.debug(f'Body: {response.content}')

        return response


    def b1host_status_summary(self, name="", id="", tags=False):
        '''
        Get B1 Hosts status information for one or more Hosts

        Parameters:
            name (ste): Display name of Host
            id (str): id of a specific Host
            tags (bool): include tags in report
        
        Returns:
            rpt: Dict of translated status elements
        '''
        rpt = None

        # Get b1host Data
        if name:
            name_filter = 'display_name=="' + name + '"'
            response = self.get('/detail_hosts', _filter=name_filter)
        elif id:
            response = self.get('/detail_hosts', id=id)
        else:
            response = self.get('/detail_hosts')
        
        if response.status_code in self.return_codes_ok:
            rpt = self.b1host_status_rpt(response.json(), tags=tags)
        else:
            logging.error(f'Response code: {response.status_code}, Data: {response.text}')
            rpt = None
    
        return rpt


    def b1host_status(self, b1host_data):
        '''
        Translate status info in JSON data for an b1host

        Parameters:
            b1host_data (dict): Data for individual b1host
        
        Returns:
            b1host_status: Dict of translated status elements
        '''
        b1host_status = {}
        b1host_comp_state = ''
        b1host_configs = []
        
        b1host_comp_state = b1host_data.get('composite_status')
        if not b1host_comp_state:
            b1host_comp_state = 'No state information'
                        
        if 'configs' in b1host_data.keys():
            b1host_configs = b1host_data.get('configs')

        b1host_status = { 'b1host state': b1host_comp_state,
                          'configs': b1host_configs } 
        
        return b1host_status
    

    def b1host_service_status(self, b1host_data):
        '''
        Translate service status info in JSON data for an b1host

        Parameters:
            b1host_data (dict): Data for individual b1host
        
        Returns:
            b1host_services: Dict of translated status elements
        '''
        b1host_services = {}
        service_name = ''
        service_type = ''
        status = ''
        message = ''
        service_version = None

        # Check for servicelication status data
        if 'services' in b1host_data.keys():
            for service in b1host_data['services']:
                service_name = service.get('service_name')
                service_type = service.get('service_type')
                service_version = service.get('current_version')

                # Check whether service is enabled
                if 'status' in service.keys():
                    status = service['status'].get('status')
                    message = service['status'].get('message')


                # Add version info if available
                if message:
                    b1host_services.update( { service_name: { 
                                                'service_type': service_type,
                                                'status': status,
                                                'message': message,
                                                'version': service_version } 
                                            } )
                else:
                    b1host_services.update( { service_name: { 
                                                'server_type': service_type,
                                                'status': status,
                                                'version': service_version }
                                            } )

        else:
            b1host_services = {}
        
        return b1host_services
   

    def b1host_status_rpt(self, json_data, tags=False):
        '''
        Build  status report from GET /detail_hosts data
        Note: Undocumented API call use with caution

        Parameters:
            json_data (json): API JSON data for B1 Hosts call
            tags (bool): Include tags in response, default False
        
        Returns:
            rpt: Dict of status elements
        '''
        rpt = {}
        b1host_name = ""
        b1host_status = {}
        b1host_services = {}

        if json_data:
            results = json_data.get('results')
            if not isinstance(results, list):
                results = [ results ]
            # Build report 
            for b1host in results:
                b1host_services = {}
                b1host_name = b1host.get('display_name')
                if b1host_name:
                    b1host_status = self.b1host_status(b1host)
                    b1host_services = self.b1host_service_status(b1host)

                    rpt.update( { b1host_name: { 'status': b1host_status,
                                          'id': b1host.get('id'),
                                          'host_type': b1host.get('host_type'),
                                          'ip_address': b1host.get('ip_address'), 
                                          'pool': b1host.get('pool'),
                                          'nat_ip': b1host.get('nat_ip'),
                                          'version': b1host.get('current_version'),
                                          'last_seen': b1host.get('last_seen'),
                                          'services': b1host_services }
                                } )
                if tags:
                    rpt[b1host_name].update({'tags': b1host.get('tags')})
        else:
            rpt = None

        return rpt

    
    def b1host_uptime(self, name="", ophid=True):
        '''
        Get the uptime for a b1host

        Note: this currently uses the ophid, if set to False this may
              generate an error

        Parameters:
            name (str): Display Name of b1host
            ophid (bool): Defaults to True to use the ophid rather than id
        
        Returns:
            Number of seconds as a string
        '''
        uptime = None
        b1hostid = self.get_b1host_id(name=name, ophid=ophid)
        url = 'https://csp.infoblox.com/atlas-status-service/v1/getsummary'
        if ophid:
            body = '{"objectID":["' + b1hostid +'"],"objectType":["Onprem Host ID"],"event_key":["health-collector/heartbeat/"]}'
        else:
            body = '{"objectID":["' + b1hostid +'"],"objectType":["Host ID"],"event_key":["health-collector/heartbeat/"]}'
        response = self._apipost(url, body=body)
        if response.status_code in self.return_codes_ok:
            uptime = response.json()['results'][0]['metadata']['hostUptime']
        
        return uptime


    def get_service_state(self, service_name=''):
        '''
        Get status of a service

        Parameters:
            service (str): Service Name
        
        Returns:
            requests response object
        '''
        service_status = ''

		# Filter on service_name if provided
        if service_name:
            filter = f'name=="{service_name}"'
            logging.debug(f'Applying filter: {filter}')
            response = self.get('/services', _filter=filter)
        else:
            response = self.get('/services')

        # Check repsone
        if response.status_code in self.return_codes_ok:
            service_status = response.json()
        else:
            logging.debug(f'HTTP Error occured. {response.status_code}')
            logging.debug(f'Body: {response.content}')
        
        return service_status


    def manage_service(self, service_name="", action="status"):
        '''
        Perform action on named b1host for specified service

        Parameters:
            service_name (str): service Name
            action (str): action to perform for service
        
        Returns:
            bool
        '''
        result = False
        actions = [ 'status' ]
        # actions = [ 'status', 'disable', 'enable', 'stop', 'start' ]

        if action in actions:
           if action == "status":
                response = self.get_service_state(service_name=service_name)
                if response:
                    result = response
                else:
                    logging.error(f'Service: {service_name} not found')
                    result = False
           elif action == "disable":
               result = self.disable_service(service_name=service_name)
           elif action == "enable":
               result = self.enable_service(service_name=service_name)
           elif action == "start":
               result = self.service_process_control(service_name=service_name,
                                                     action="start") 
           elif action == "stop":
               result = self.service_process_control(service_name=service_name, 
                                                     action="stop") 
           else:
               logging.error(f'Action: {action} not implemented')
               result = False
        else:
            logging.error(f'Action: {action} not supported')
            logging.info(f'Supported actions: {actions}')
            result = False

        return result

    """

    def disable_service(self, service_name=''):
        '''
        Disable specified service on named b1host

        Parameters:
            name (str): display_name of b1host
            service (str): service Name, e.g. DNS
        
        Returns:
            bool
        '''
        status = False
        service_type = ''

        # Check service supported and get Get servicelication_type
        if service_name in self.b1host_service_NAMES.keys():
            service_type = self.b1host_service_NAMES[service]
        elif service_name in self.b1host_services.keys():
            service_type = service

        if service_type:
            # Get id of b1host
            filter = f'display_name=="{name}"'
            response = self.get('/hosts', 
                                _filter=filter)
            if response.status_code in self.return_codes_ok:
                b1host_data = response.json()['result']
                id = b1host_data[0]['id']
                logging.debug(f'B1 Host id = {id}')

                # Build body
                body = { 'display_name': name, 
                         'servicelications': [ { 'servicelication_type': service_type,
                                             'disabled': '1', 
                                             'state': { 'desired_state': '0' } 
                                           } ] } 
                
                # Update desired b1host
                response = self.update('/hosts',
                                       id=id,
                                       body=json.dumps(body))
                if response.status_code in self.return_codes_ok:
                    logging.debug(f'b1host: {name}, service: {service}, service_type: {service_type}')
                    status = True
                else:
                    logging.error(f'{response.status_code}: {response.text}')

            else:
                logging.error(f'b1host {name} not found.')
                status = False
        else:
            logging.error(f'service {service} not supported.')
            status = False
        
        return status


    def enable_service(self, name="", service=""):
        '''
        Enable specified service on named b1host

        Parameters:
            name (str): display_name of b1host
            service (str): service Name, e.g. DNS
        
        Returns:
            bool
        '''
        status = False
        service_type = ''

        # Check service supported and get Get servicelication_type
        if service in self.b1host_service_NAMES.keys():
            service_type = self.b1host_service_NAMES[service]
        elif service in self.b1host_services.keys():
            service_type = service

        if service_type:
            # Get id of b1host
            filter = f'display_name=="{name}"'
            response = self.get('/hosts', 
                                _filter=filter)
            if response.status_code in self.return_codes_ok:
                b1host_data = response.json()['result']
                id = b1host_data[0]['id']
                logging.debug(f'B1 Host id = {id}')

                # Build body
                body = { 'display_name': name, 
                         'servicelications': [ { 'servicelication_type': service_type,
                                             'disabled': '0', 
                                             'state': { 'desired_state': '1' } 
                                           } ] } 
                
                # Update desired b1host
                response = self.update('/hosts',
                                       id=id,
                                       body=json.dumps(body))
                if response.status_code in self.return_codes_ok:
                    logging.debug(f'b1host: {name}, service: {service}, service_type: {service_type}')
                    status = True
                else:
                    logging.error(f'{response.status_code}: {response.text}')

            else:
                logging.error(f'b1host {name} not found.')
                status = False
        else:
            logging.error(f'service {service} not supported.')
            status = False
        
        return status
    

    def service_process_control(self, service_name="", action=""): 
        '''
        Start or stop a service

        Parameters:
            service_name (str): Name of service
        
        Returns:
            bool 
        '''
        status = False
        actions = [ 'start', 'stop' ]
        service_status = {}
        id = ''
        pool_id = ''
        service_type = ''
        current_state = ''
        desired_state = ''
        
        if action.lower() in actions:
            # Get required service elements
            service_status = self.b1host_service_status(service_name=service_name)
            if service_status:
                currrent_state = service_status.get('composite_status')
                desired_state = service_status.get('desired_status')
                if desired_state == action.lower():
                    logging.info(f'Service {service_name} already set to {desired_state}')
                    logging.info(f'Current state: {current_state}')
                    status = True
                else:
                    id = service_status.get('id')
                    service_type = service_status.get('service_type')
                    logging.debug(f'Service id = {id}')
                    logging.debug(f'service status: {service_name} service is {current_state}')
                    # Check whether service is disabled
                if 'disabled' not in service_status:
                    # Build body
                    body = { 'display_name': service_name, 
                            'servicelications': [ { 'servicelication_type': service_type,
                                                'disabled': '0', 
                                                'state': 
                                                    { 'desired_state': actions[action] } 
                                            } ] } 
                    
                    # Update desired b1host
                    response = self.update('/hosts',
                                        id=id,
                                        body=json.dumps(body))
                    if response.status_code in self.return_codes_ok:
                        logging.debug(f'b1host: {service_name}, service: {service}, service_type: {service_type}')
                        status = True
                    else:
                        logging.error(f'{response.status_code}: {response.text}')
                        status = False
                else:
                    logging.info(f'service: {service} on b1host: {name} {service_status}')
                    status = False

            else:
                logging.error(f'service {service} not supported.')
                status = False
        else:
            logging.error(f'Action: {action} not supported')
            status = False

        return status
    
    """