#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 Requirements:
   Python3 with re, ipaddress, requests and sqlite3 modules

 Author: Chris Marrison

 Date Last Updated: 20200605

 Todo:

 Copyright (c) 2018 Chris Marrison / Infoblox

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
__version__ = '0.0.2
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import bloxone
import logging
import os
import re
import datetime
import ipaddress

# ** Global Vars **

class b1ddi(bloxone.b1):

    def on_prem_hosts(self, id="", filter="", tfilter=""):
        '''
        Method to retrieve On Prem Hosts

        Parameters:
            filter (str):   Filter based on data fields
            tfilter (str):  Tag filter

        Returns:
           status_code (obj): status code or zero on exception
           body (str): Raw JSON or "Exception occurred." upon exception
        '''

        # Start build of URL
        url = self.host_url + '/on_prem_hosts'
        
        # if id:
            # url = url + ''
        if filter:
            url = url + '?_filter=' + filter
        if filter and tfilter:
            url = url + '&_tfilter=' + tfilter
        elif tfilter:
            url = url + '?_tfilter=' + tfilter

        # Call BloxOne API
        status_code, body = self.apiget(url)

        # Return response code and body text
        return status_code, body


    def ip_space(self, id="", filter="", tfilter=""):
        '''
        Method to retrieve On Prem Hosts

        Parameters:
            filter (str):   Filter based on data fields
            tfilter (str):  Tag filter

        Returns:
           status_code (obj): status code or zero on exception
           body (str): Raw JSON or "Exception occurred." upon exception
        '''

        # Start build of URL
        url = self.ipam_url + '/ip_space'
        
        if id:
            url = url + '/' + id
        if filter:
            url = url + '?_filter=' + filter
        if filter and tfilter:
            url = url + '&_tfilter=' + tfilter
        elif tfilter:
            url = url + '?_tfilter=' + tfilter
        
        print(url)

        # Call BloxOne API
        status_code, body = self.apiget(url)

        # Return response code and body text
        return status_code, body

