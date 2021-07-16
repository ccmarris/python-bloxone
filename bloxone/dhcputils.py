#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:
    Simple utility functions for data type validation, domain handling,
    and data normalisationa specifically with the aim of supporting
    queries to TIDE and Dossier.

 Requirements:
   Python3 with re, ipaddress, requests 

 Author: Chris Marrison

 Date Last Updated: 20210714

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
__version__ = '0.0.1'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import logging
import ipaddress
from re import I

# ** Global Vars **
# DHCP Encoding Utils

class dhcp_encode():
    '''
    Class to assist with Hex Encoding of 
    DHCP Options and sub_options
    '''
    def __init__(self) -> None:
        self.opt_types = [ 'string', 'ipv4_address' ]
        return


    def validate_ip(self, ip):
        '''
        Validate input data is a valid IP address

        Parameters:
            ip (str): ip address as a string

        Returns:
            bool: Return True for valid and False otherwise

        '''
        try:
            ipaddress.ip_address(ip)
            result = True
        except ValueError:
            result = False
        return result


    def ipv4_address_to_hex(self, ipv4):
        '''
        '''
        if self.validate_ip(ipv4):
            ip = ipaddress.ip_address(ipv4)
            hex = '{:x}'.format(ip)
        else:
            hex = None

        return hex


    def string_to_hex(self, string):
        '''
        '''
        s = string.encode('utf-8')
        return s.hex()


    def optcode_to_hex(self, optcode):
        '''
        '''
        hex_opt = '{:02x}'.format(int(optcode))
        return hex_opt


    def hex_length(self, hex_string):
        '''
        '''
        hex_len = '{:02x}'.format(int(len(hex_string) / 2))
        return hex_len


    def encode_data(self, sub_opt, array=False):
        '''
        '''
        hex_data = ''
        if sub_opt['type'] in self.opt_types:
            type_to_hex = eval('self.' + sub_opt['type'] + '_to_hex')
        else:
            logging.error(f'Unsupported Option Type {sub_opt["type"]}')
            logging.info('Unsupported option type, ' +
                         'attempting to process as string')
            type_to_hex = eval('self.string_to_hex')

        if array:
            for item in sub_opt['data'].split(','):
                hex_data = hex_data + type_to_hex(sub_opt['data'])       
        else:
            hex_data = type_to_hex(sub_opt['data'])       

        return hex_data


    def encode_sub_option(self, sub_opt, array=False, data_only=False):
        '''
        '''
        # Local variables
        hex = ''
        hex_opt = ''
        hex_len = ''
        hex_data = ''

        if data_only:
            hex_data = self.encode_data(sub_opt)
        else:
            if sub_opt['code'] in range(1, 256):
                hex_opt = self.optcode_to_hex(sub_opt['code'])
                hex_data = self.encode_data(sub_opt)
                hex_len = self.hex_length(hex_data)
            else:
                # Log error (or potentially raise exception or something)
                logging.error(f'Option Code: {sub_opt["code"]} out of range.')
        
        hex = hex_opt + hex_len + hex_data
        return hex


    def encode_dhcp_option(self, 
                           sub_opt_defs=[], 
                           padding=False,
                           pad_bytes=1,
                           encapsulate=False,
                           id=None ):
        '''
        '''
        hex = ''

        # Encode sub_options
        for opt in sub_opt_defs:
            hex = hex + self.encode_sub_option(opt) 
        
        if encapsulate:
            total_len = self.hex_length(hex)
            main_opt = self.optcode_to_hex(id)
            hex = main_opt + total_len + hex

        return hex