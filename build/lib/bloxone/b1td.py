#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 BloxOne Threat Defence API Wrapper Class and Helpers

 Author: Chris Marrison

 Date Last Updated: 20211203

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
__version__ = '0.3.3'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import bloxone
import logging
import datetime
import json

# ** Exceptions **

class CountryISOCodeNotFound(Exception):
    '''
    ISO Code for Country not found
    '''
    pass


# b1td class
class b1td(bloxone.b1):
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
        url = self.tide_url + objpath
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        response = self._apiget(url)

        return response


    def post(self, objpath, body=""):
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

        # Make API Call
        response = self._apipost(url, body)

        return response


   # *** Helper Methods ***

    def threat_classes(self, **params):
        '''
        Get list of threat classes

        Parameters:

        Returns:
            response object: Requests response object
        '''

        # Local Variables
        objpath = '/data/threat_classes'

        # Build url
        url = self.tide_url + objpath

        # Make API Call
        response = self._apiget(url)

        return response


    def threat_properties(self, threatclass="", **params):
        '''
        Get list of threat properties

        Parameters:
            threatclass (str): Threat Class

        Returns:
            response object: Requests response object
        '''

        # Local Variables
        objpath = '/data/properties'

        # Build url
        url = self.tide_url + objpath
        if threatclass:
            url = url + '?class=' + threatclass

        # Make API Call
        response = self._apiget(url)

        return response

    def threat_counts(self):
        '''
        Query Infoblox TIDE for active threat counts

        Returns:
            response object: Requests response object
        '''
        # Build URL
        url = self.tide_url + '/data/threat/counts'

        # Make API Call
        response = self._apiget(url)

        return response


    def historical_threat_counts(self):
        '''
        Query Infoblox TIDE for historical threat counts

        Returns:
            response object: Requests response object
        '''
        # Build URL
        url = self.tide_url + '/data/threat/counts/historical'

        # Make API Call
        response = self._apiget(url)

        return response


    def default_ttl(self):
        '''
        '''
        url = self.tide_url + '/data/default/ttl'
        response = self._apiget(url)

        return response


    def querytide(self, datatype, query, **params):
        '''
        Query Infoblox TIDE for all avaialble threat data
        related to query.

        Parameters:
            datatype (str): "host", "ip" or "url"
            query (str): query data

        Returns:
            response object: Requests response object
        '''
        objpath = '/data/threats/'

        # Build URL
        url = self.tide_url + objpath
        url = url + datatype + '?' + datatype + '=' + query
        url = self._add_params(url, first_param=False, **params)

        # Make API Call
        response = self._apiget(url)

        return response


    def querytideactive(self, datatype, query, **params):
        '''
        Query Infoblox TIDE for "active" threat data
        i.e. threat data that has not expired at time of call

        Parameters:
            datatype (str): "host", "ip" or "url"
            query (str): query data

        Returns:
            response object: Requests response object
        '''
        objpath = '/data/threats/'
        now = datetime.datetime.now()

        # Build URL
        url = self.tide_url + objpath
        url = url + datatype + '?' + datatype + '=' + query
        url = url + '&expiration=' + now.strftime('%Y-%m-%dT%H:%M:%SZ')
        url = self._add_params(url, first_param=False, **params)

        # Make API Call
        response = self._apiget(url)

        return response


    def querytidestate(self, datatype, query, **params):
        '''
        Query Infoblox TIDE State Tables for specific query

        Parameters:
            datatype (str): "host", "ip" or "url"
            query (str): query data

        Returns:
            response object: Requests response object
        '''
        objpath = '/data/threats/state/'

        # Build URL
        url = self.tide_url + objpath
        url = url + datatype + '?' + datatype + '=' + query
        url = self._add_params(url, first_param=False, **params)

        # Make API Call
        response = self._apiget(url)

        return response


    def tideactivefeed(self, 
                       datatype, 
                       profile="", 
                       threatclass="",
                       threatproperty="",
                       **params ):
        '''
        Bulk "active" threat intel download from Infoblox TIDE state tables
        for specified datatype.

        Parameters:
            datatype (str): "host", "ip" or "url"
            profile (str, optional): Data provider
            threatclass (str, optional): tide data class
            threatproperty (str, optional): tide data property

        Returns:
            response object: Requests response object
        '''
        objpath = '/data/threats/state/'

        # Build URL
        url = self.tide_url + objpath
        url = url + datatype 
        if profile or threatclass or threatproperty:
            url = url + '?'
            if profile:
                url = url + '&profile=' + profile
            if threatclass:
                url = url + '&class=' + threatclass
            if threatproperty:
                url = url + '&property=' + threatproperty
            url = self._add_params(url, first_param=False, **params) 
        else:
            url = self._add_params(url, **params) 

        # Make API Call
        response = self._apiget(url)

        return response


    def tidedatafeed(self, 
                    datatype, 
                    profile="", 
                    threatclass="",
                    threatproperty="",
                    **params):
        '''
        Bulk threat intel download from Infoblox TIDE 
        for specified datatype. Please use wisely.

        Parameters:
            datatype (str): "host", "ip" or "url"
            profile (str, optional): Data provider
            threatclass (str, optional): tide data class
            threatproperty (str, optional): tide data property

        Returns:
            response object: Requests response object
        '''
        objpath = '/data/threats/'

        # Build URL
        url = self.tide_url + objpath
        url = url + datatype 
        if profile or threatclass or threatproperty:
            url = url + '?'
            if profile:
                url = url + '&profile=' + profile
            if threatclass:
                url = url + '&class=' + threatclass
            if threatproperty:
                url = url + '&property=' + threatproperty
            url = self._add_params(url, first_param=False, **params) 
        else:
            url = self._add_params(url, **params) 

        # Make API Call
        response = self._apiget(url)

        return response

    # ** Dossier Methods **

    def dossier_sources(self):
        '''
        Get Sources for Dossier

        Returns:
            response object: Requests response object
        '''
        url = self.dossier_url + '/sources'
        response = self._apiget(url)

        return response


    def dossier_target_sources(self, type='host'):
        '''
        Get supported target types for Dossier 

        Parameters:
            type (str): target type

        Returns:
            response object: Request response object
        '''
        url = self.dossier_url + '/sources/target/' + type
        response = self._apiget(url)

        return response


    def dossier_target_types(self):
        '''
        Get supported target types for Dossier 

        Returns:
            response object: Request response object
        '''
        url = self.dossier_url + '/targets'
        response = self._apiget(url)

        return response


    def dossierquery(self, query, type="host", sources="all", wait=True):
        '''
        Simple Dossier Query
        
        Parameters:
            query (str or list): single query or list of same type
            type (str): "host", "ip" or "url"
            sources (str): set of sources or "all"

        Returns:
            response object: Requests response object
        '''

        if isinstance(wait, bool) and wait:
            wait = 'true'
        else:
            wait = 'false'
        url = self.dossier_url + '/jobs?wait=' + wait
        # Create body
        if sources == "all":
            response = self.dossier_target_sources(type=type)
            if response.status_code in self.return_codes_ok:
                sources = []
                for source in response.json().keys():
                    if response.json()[source]:
                        sources.append(source)
                logging.debug("Sources retrieved: {}".format(sources))
            else:
                sources = ['atp', 'activity', 'dns', 'geo', 'pdns', 'ptr', 
                           'rwhois', 'whopis', 'inforank', 'rpz_feeds', 
                           'ssl_cert', 'infoblox_web_cat', 'custom_lists',
                           'whitelist']
                logging.debug("Failed to retrieve sources, using " 
                              + "limited list {}".format(sources))
        else:
            if not isinstance(sources, list):
                source_list = []
                source_list.append(sources) 
                sources = source_list

        # Check for group of queries
        if isinstance(query, list): 
            body = {"target": {"group": {"type": type,
                    "sources": sources,
                    "targets": query  } } }
        else:
            body = {"target": {"one": {"type": type,
                    "sources": sources, "target": query  } } }

        body = json.dumps(body)
        logging.debug(f'Body: {body}')

        response = self._apipost(url, body)

        return response


    # *** threat enrichment 

    def threat_actor(self, name):
        '''
        Get Threat Actor details

        Parameters:
            name(str): Name of Threat Actor
        
        Returns:
            response object: Requests response object
        '''

        url = self.threat_enrichment_url + '/threat_actor/lookup?name=' + name
        response = self._apiget(url)

        return response


    def expand_mitre_vector(self, mitre):
        '''
        Expand MITRE Vector details

        Parameters:
            mitre(str): MITRE Vector
        
        Returns:
            response object: Requests response object
        '''

        url = self.threat_enrichment_url + '/mitre/lookup'
        body = '"' + mitre + '"'
        logging.debug("URL: {}, Body: {}".format(url,body))
        response = self._apipost(url, body)

        return response

    def get_countries(self):
        '''
        Get Countries and Country Code Data

        Parameters:
            None
        
        Returns:
            response object: Requests response object
        '''
        url = self.tide_url + '/data/set/countries'
        logging.debug("URL: {}".format(url))

        return self._apiget(url)


    def get_country_isocode(self, country=""):
        '''
        Get ISO Code for specified country

        Parameters:
            country (str): Name of Country
        
        Returns:
            isocode (str): ISO Code of Country or None if no match 
        '''
        isocode = ''

        response = self.get_countries()
        if response.status_code in self.return_codes_ok:
            country_codes = response.json()['country']
            country_record = next((c for c in country_codes 
                                if c['name'].casefold() == country.casefold()), 
                                {} )
            isocode = country_record.get('iso_code')

        else:
            logging.error(f'Unable to retrieve country list')
            isocode = None
        
        return isocode
            

    def get_country_ips(self, country='', **params):
        '''
        Get IPs for specified countries or complete dataset

        Parameters:
            country: Country or Country Code to retrieve
        
        Returns:
            response object: Requests response object
        
        Raises:
            CountryISOCodeNotFound
        '''
        iso_code = ''
        url = self.tide_url + '/data/set/countryip'
        
        if country:
            if len(country) == 2:
                # Assume country isocode
                iso_code = country
            else:
                # Assume country name
                iso_code = self.get_country_isocode(country=country)
            if iso_code:
                url = self._add_params(url, first_param=True, country=iso_code)
            else:
                raise CountryISOCodeNotFound(f'No match for country: {country}')

        return self._apiget(url)


