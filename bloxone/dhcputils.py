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

 Date Last Updated: 20210716

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
__version__ = '0.1.1'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import logging
import ipaddress
import bloxone
from re import I

# ** Global Vars **
# DHCP Encoding Utils

class dhcp_encode():
    '''
    Class to assist with Hex Encoding of 
    DHCP Options and sub_options
    '''
    def __init__(self) -> None:
        self.opt_types = [ 'string', 
                           'ipv4_address', 
                           'ipv6_address',
                           'boolean',
                           'int8',
                           'uint8',
                           'int16',
                           'uint16',
                           'int32',
                           'uint32',
                           'fqdn',
                           'binary',
                           'empty' ]

        self.fqdn_re, self.url_re = bloxone.utils.buildregex()
        return


    def validate_ip(self, ip):
        '''
        Validate input data is a valid IP address
        (Supports both IPv4 and IPv6)

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


    # IP encondings
    def ip_to_hex(self, ip):
        '''
        '''
        if self.validate_ip(ip):
            ip = ipaddress.ip_address(ip)
            hex_value = '{:x}'.format(ip)
        else:
            hex_value = None

        return hex_value

    # Methods for IPv4 and IPv6
    def ipv4_address_to_hex(self, ipv4):
        '''
        '''
        return self.ip_to_hex(ipv4)
        
    
    def ipv6_address_to_hex(self, ipv6):
        '''
        '''
        return self.ip_to_hex(ipv6)


    # String/text encoding
    def string_to_hex(self, string):
        '''
        '''
        s = string.encode('utf-8')
        return s.hex()


    # Boolean encoding
    def boolean_to_hex(self, flag):
        '''
        '''
        # Handle Bool or str
        if not isinstance(flag, bool):
            if isinstance(flag, str):
                if flag.casefold() == 'true': 
                    flag = True
                else:
                    flag = False
            else:
                flag = False

        # Set hex value     
        if flag:
            hex = '01'
        else:
            hex = '00'
        
        return hex


   # integer encodings 
    def int_to_hex(self, i, size = 8):
        '''
        '''
        hex_value = ''
        i = int(i)
        i_sizes = [ 8, 16, 32 ]
        if size in i_sizes:
            max_bits = size - 1
            no_bytes = size // 4
            fmt = f'{{:0{no_bytes}x}}'
            if i > 0 and i < (2**max_bits):
                hex_value = fmt.format(int(i))
            elif abs(i) <= (2**max_bits):
                hex_value = fmt.format(int(abs(i) + (2**max_bits))) 
            else:
                raise TypeError(f'{i} is out of range for int{size} type')

        return hex_value 


    def uint_to_hex(self, i, size = 8):
        '''
        '''
        i = int(i)
        i_sizes = [ 8, 16, 32 ]
        if size in i_sizes:
            max_size = 2**size
            no_bytes = size // 4
            fmt = f'{{:0{no_bytes}x}}'
            if i < max_size:
                hex = fmt.format(i + (2**size))
            else:
                raise TypeError(f'{i} is out of range for uint{size} type')

        return hex 


    # Methods for intX and uintX
    def int8_to_hex(self, value):
        return self.int_to_hex(value, size=8)


    def uint8_to_hex(self, value):
        return self.uint_to_hex(value, size=8)


    def int16_to_hex(self, value):
        return self.int_to_hex(value, size=16)


    def uint16_to_hex(self, value):
        return self.uint_to_hex(value, size=16)


    def int32_to_hex(self, value):
        return self.int_to_hex(value, size=32)


    def uint32_to_hex(self, value):
        return self.uint_to_hex(value, size=32)


    # FDQN Encoding
    def fqdn_to_hex(self, fqdn):
        '''
        '''
        hex = ''
        hex_label = ''

        # Validate FQDN
        if bloxone.utils.validate_fqdn(fqdn, self.fqdn_re):
            if fqdn.endswith("."):
                # strip exactly one dot from the right, if present
                fqdn = fqdn[:-1]
            # Encode labels
            for label in fqdn.split("."):
                hex_label = self.string_to_hex(label)    
                hex_len = self.hex_length(hex_label)
                hex += hex_len + hex_label

            # Terminate with null byte
            hex += '00'

        else:
            logging.error(f'{fqdn} is not a valid FQDN')
        
        return hex


    # Binary Encoding
    def binary_to_hex(self, data):
        '''
        '''
        # Should put some format of checking
        return data

    
    # Empty Encoding
    def empty_to_hex(self, data):
        '''
        '''
        if data:
            data = ''
        return data
        

    # Code and Length encoding
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


    # Encoding Methods
    def encode_data(self, sub_opt, padding=False, pad_bytes=1):
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
        
        # Check for array attribute
        if 'array' in sub_opt.keys():
            array = sub_opt['array']
        else:
            logging.debug(f'No array attribute for option: {sub_opt["code"]}')
            array = False

        # Encode data
        if array and (len(sub_opt['data'].split(',')) > 1):
            for item in sub_opt['data'].split(','):
                hex_data += type_to_hex(item)
        else:
            hex_data = type_to_hex(sub_opt['data'])       
        
        if padding:
            hex_data += pad_bytes * '00'

        return hex_data


    def encode_sub_option(self, sub_opt, 
                          data_only=False,
                          padding=False,
                          pad_bytes=1):
        '''
        '''
        # Local variables
        hex_value = ''
        hex_opt = ''
        hex_len = ''
        hex_data = ''

        if data_only:
            hex_data = self.encode_data(sub_opt)
            hex_value = hex_data
        else:
            if int(sub_opt['code']) in range(0, 256):
                hex_opt = self.optcode_to_hex(sub_opt['code'])
                hex_data = self.encode_data(sub_opt)
                hex_len = self.hex_length(hex_data)
                hex_value = hex_opt + hex_len + hex_data
            else:
                # Log error (or potentially raise exception or something)
                logging.error(f'Option Code: {sub_opt["code"]} out of range.')
                hex_value = ''
        
        return hex_value


    def encode_dhcp_option(self, 
                           sub_opt_defs=[], 
                           padding=False,
                           pad_bytes=1,
                           encapsulate=False,
                           id=None ):
        '''
        '''
        hex_value = ''

        # Encode sub_options
        for opt in sub_opt_defs:
            hex_value += self.encode_sub_option(opt) 
        
        if encapsulate:
            total_len = self.hex_length(hex)
            main_opt = self.optcode_to_hex(id)
            hex_value = main_opt + total_len + hex_value

        return hex_value


    def tests(self):
        '''
        '''
        test_data = [ { 'code': '1', 'type': 'string', 'data': 'AABBDDCCEEDD-aabbccddeeff' },
                      { 'code': '2', 'type': 'ipv4_address', 'data': '10.10.10.10' },
                      { 'code': '3', 'type': 'ipv4_address', 'data': '10.10.10.10,11.11.11.11', 'array': True },
                      { 'code': '4', 'type': 'boolean', 'data': True },
                      { 'code': '5', 'type': 'int8', 'data': '22' },
                      { 'code': '5', 'type': 'int8', 'data': '-22' },
                      { 'code': '6', 'type': 'uint8', 'data': '22' },
                      { 'code': '7', 'type': 'int16', 'data': '33'},
                      { 'code': '8', 'type': 'int16', 'data': '33'},
                      { 'code': '9', 'type': 'uint16', 'data': '33'}, 
                      { 'code': '10', 'type': 'int32', 'data': '44'}, 
                      { 'code': '11', 'type': 'uint32', 'data': '-44'}, 
                      { 'code': '12', 'type': 'uint32', 'data': '44'}, 
                      { 'code': '13', 'type': 'fqdn', 'data': 'www.infoblox.com' },
                      { 'code': '14', 'type': 'binary', 'data': 'DEADBEEF' },
                      { 'code': '15', 'type': 'empty', 'data': ''},
                      { 'code': '16', 'type': 'ipv6_address', 'data': '2001:DB8::1' },
                      { 'code': '17', 'type': 'ipv6_address', 'data': '2001:DB8::1,2001:DB8::2', 'array': True } ]

        print(f'Encoding types supported: {self.opt_types}')
        print()
        print('Non-array tests:')
        for data_test in test_data:
            result = self.encode_data(data_test)
            hex_len = self.hex_length(result)
            print(f'Type: {data_test["type"]}: {data_test["data"]}, ' +
                  f'Encoded: {result}, Length(hex): {hex_len}')
        
        print()
        # Padding Test
        test_data = { 'code': '99', 'type': 'string', 'data': 'AABBCCDD' }
        result = self.encode_data(test_data, padding=True)
        print(f'Padding test (1 byte), type string: {test_data["data"]} {result}')
        # Full encode test
        test_data = [ { 'code': '1', 'type': 'string', 'data': 'AABBDDCCEEDD-aabbccddeeff' },
                      { 'code': '2', 'type': 'ipv4_address', 'data': '10.10.10.10' },
                      { 'code': '3', 'type': 'ipv4_address', 'data': '10.10.10.10,11.11.11.11', 'array': True },
                      { 'code': '4', 'type': 'boolean', 'data': True },
                      { 'code': '5', 'type': 'int8', 'data': '22' } ]
        result = self.encode_dhcp_option(test_data)
        print(f'Full encoding of sample: {result}')

        return
                

