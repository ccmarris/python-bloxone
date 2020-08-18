#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 BloxOne DDI API Wrapper Class and Helpers

 Author: Chris Marrison

 Date Last Updated: 20200810

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
__version__ = '0.1.5'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import bloxone
import logging
import json
import datetime

# ** Global Vars **

class b1td(bloxone.b1):
    '''
    BloxOne ThreatDefence API Wrapper
    Covers TIDE and Dossier
    '''

    # Generic Methods
    def get(self, objpath, action="", **params):
        '''
        Generic get object wrapper for TIDE data objects

        Parameters:
            objpath (str):  Swagger object path
            action (str):   Optional object action
        
        Returns:
            response (obj): Requests response object
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
            response (obj): Requests response object
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
            response (obj): Requests response object
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
            response (obj): Requests response object
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

    """
    (Currently not implemented)
    def threat_stats(self, period="daily", **paramas):
        '''
        Query Infoblox TIDE for threat class stats

        Parameters:
            period (str): one of ['daily', 'weekly', 'monthly']

        Returns:
            response (obj): Requests response object
        '''
        objpath = '/data/dashboard/'

        # Build URL
        url = self.tide_url + objpath
        url = url + period 
        # url = url + period + '_threats_by_class'

        # Make API Call
        response = self._apiget(url)

        return response
    """

    def querytide(self, datatype, query, **params):
        '''
        Query Infoblox TIDE for all avaialble threat data
        related to query.

        Parameters:
            datatype (str): "host", "ip" or "url"
            query (str): query data

        Returns:
            response (obj): Requests response object
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
            response (obj): Requests response object
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
            response (obj): Requests response object
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
            response (obj): Requests response object
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


"""
Not documented and returns Not Implemented
    def dossierquery(self, type="host", sources="all"):
        '''
        Simple Dossier Query
        
        Parameters:
            query (str): query data
            type (str): "host", "ip" or "url"
            sources (str): set of sources or "all"

        Returns:
            response (obj): Requests response object
        '''
        url = self.dossier_url
        # Create body
        if sources == "all":
            sources = ('"alexa","atp","ccb","dns","gcs","geo","gsb",
                        "isight","malware_analysis","ptr","pdns","rwhois",
                        "whois","inforank"')
        else:
            sources = '"'+sources+'"'

        body = ('{"target": {"one": {"type": "'
                + type + '", "target": "'
                + query + '", "sources": ['+sources+'] }}}, "
                + "options":{}}')

        response = self._apipost(url, body)

        return response
    """


