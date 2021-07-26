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

 Date Last Updated: 20210721

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
__version__ = '0.1.4'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import logging
import ipaddress
import os
import yaml
import binascii
import bloxone

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
        Encode an IPv4 or IPv6 address to hex

        Parameters:
            ip (str): IPv4 or IPv6 address as a string
        
        Returns:
            hex encoding as string
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
        Encode an IPv4 address to hex

        Parameters:
            ipv4 (str): IPv4 address as a string
        
        Returns:
            hex encoding as string
        '''
        return self.ip_to_hex(ipv4)
        
    
    def ipv6_address_to_hex(self, ipv6):
        '''
        Encode an IPv6 address to hex

        Parameters:
            ipv6 (str): IPv4 or IPv6 address as a string
        
        Returns:
            hex encoding as string
        '''
        return self.ip_to_hex(ipv6)


    # String/text encoding
    def string_to_hex(self, string):
        '''
        Encode a text string to hex

        Parameters:
            string (str): text string
        
        Returns:
            hex encoding as string
        '''
        s = str(string).encode('utf-8')
        return s.hex()


    # Boolean encoding
    def boolean_to_hex(self, flag):
        ''' 
        Encode boolean value as single hex byte

        Parameters:
            flag (bool/str): True or False as bool or text
        
        Returns:
            hex encoding as string
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
        Encode integer of specified size as signed int in hex

        Parameters:
            i (int): integer value to encode
            size (int): size in bits [8, 16, 32]
        
        Returns:
            hex encoding as string
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
        Encode integer of specified size as unsigned int in hex
        Uses 2's compliment if supplied with negative number


        Parameters:
            i (int): integer value to encode
            size (int): size in bits [8, 16, 32]
        
        Returns:
            hex encoding as string
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
        Encode an fdqn in RFC 1035 Section 3.1 formatted hex

        Parameters:
            fqdn (str): hostname to encode

        Returns:
            hex encoding as string
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
        Format hex string of binary/hex encoded data

        Parameters:
            data (str): data to format

        Returns:
            hex encoding as string
        '''
        hex_value = ''
        base = 16 

        # Check for binary
        if data[:2] == '0b':
            base = 2
        
        # Force hex encoding without 0x using base
        hex_value = '{:02x}'.format(int(data, base))

        return hex_value

    
    # Empty Encoding
    def empty_to_hex(self, data):
        '''
        Return empyt hex string ''

        Parameters:
            data (str): Data not to encode (should be empty)
        
        Returns:
            Empty String ''
        '''
        if data:
            data = ''
        return data
        

    # Code and Length encoding
    def optcode_to_hex(self, optcode):
        '''
        Encode Option Code in hex (1-octet)

        Parameters:
            optcode (str/int): Option Code 
        
        Returns:
            hex encoding as string
        '''
        hex_opt = '{:02x}'.format(int(optcode))
        return hex_opt


    def hex_length(self, hex_string):
        '''
        Encode Option Length in hex (1-octet)

        Parameters:
            hex_string (str): Octet Encoded Hex String
        
        Returns:
            Number of Hex Octects as hex encoded string
        '''
        hex_len = '{:02x}'.format(int(len(hex_string) / 2))
        return hex_len


    # Encoding Methods
    def encode_data(self, sub_opt, padding=False, pad_bytes=1):
        '''
        Encode the data section of a sub_option definition

        Parameters:
            sub_opt (dict): Dict containing sub option details
                            Must include 'data' and 'type' keys
            padding (bool): Whether extra 'null' termination bytes are req.
            pad_bytes (int): Number of null bytes to append

        Returns:
            Hex encoded data for specified data-type as string
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
        Encode individual sub option

        Parameters:
            sub_opt (dict): Sub Option Definition, as dict.
            data_only (bool): Encode data portion only if True
                              (Note the sub_opt dict is also checked for 
                              the 'data-only' key)
            padding (bool): Whether extra 'null' termination bytes are req.
            pad_bytes (int): Number of null bytes to append
        
        Returns:
            Encoded suboption as a hex string
        '''
        # Local variables
        hex_value = ''
        hex_opt = ''
        hex_len = ''
        hex_data = ''

        # Check whether 'data-only' is defined in sub_option
        if 'data-only' in sub_opt.keys():
            data_only = sub_opt['data-only']
        # Check whether to encode only the data or whole sub option
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
                           id=None,
                           prefix='' ):
        '''
        Encode list of DHCP Sub Options to Hex

        Parameters:
            sub_opt_defs (list): List of Sub Option definition dictionaries
            padding (bool): Whether extra 'null' termination bytes are req.
            pad_bytes (int): Number of null bytes to append
            encapsulate (bool): Add id and total length as prefix
            id (int): option code to prepend
            prefix (str): String value to prepend to encoded options
        
        Returns:
            Encoded suboption as a hex string
        '''
        hex_value = ''

        # Encode sub_options
        for opt in sub_opt_defs:
            hex_value += self.encode_sub_option(opt) 
        
        if encapsulate:
            total_len = self.hex_length(hex)
            main_opt = self.optcode_to_hex(id)
            hex_value = main_opt + total_len + hex_value
        
        if prefix:
            hex_value += prefix 

        return hex_value


    def tests(self):
        '''
        Run through encoding methods and output example results
        '''
        test_data = [ { 'code': '1', 'type': 'string',
                        'data': 'AABBDDCCEEDD-aabbccddeeff' },
                      { 'code': '2', 'type': 'ipv4_address',
                        'data': '10.10.10.10' },
                      { 'code': '3', 'type': 'ipv4_address',
                        'data': '10.10.10.10,11.11.11.11', 'array': True },
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
                      { 'code': '13', 'type': 'fqdn',
                        'data': 'www.infoblox.com' },
                      { 'code': '14', 'type': 'binary', 'data': 'DEADBEEF' },
                      { 'code': '15', 'type': 'empty', 'data': ''},
                      { 'code': '16', 'type': 'ipv6_address',
                        'data': '2001:DB8::1' },
                      { 'code': '17', 'type': 'ipv6_address',
                        'data': '2001:DB8::1,2001:DB8::2', 'array': True } ]

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
        print(f'Padding test (1 byte), type string: {test_data["data"]}' +
              f' {result}')
        # Full encode test
        test_data = [ { 'code': '1', 'type': 'string',
                        'data': 'AABBDDCCEEDD-aabbccddeeff' },
                      { 'code': '2', 'type': 'ipv4_address',
                        'data': '10.10.10.10' },
                      { 'code': '3', 'type': 'ipv4_address',
                        'data': '10.10.10.10,11.11.11.11', 'array': True },
                      { 'code': '4', 'type': 'boolean', 'data': True },
                      { 'code': '5', 'type': 'int8', 'data': '22' } ]
        result = self.encode_dhcp_option(test_data)
        print(f'Full encoding of sample: {result}')

        return
                

# *** Class to handle Vendor Option Definitions Dictionary in YAML ***
class DHCP_OPTION_DEFS():
    '''
    Class to load and handle DHCP Option Defs
    '''

    def __init__(self, cfg='vendor_dict.yaml'):
        '''
        Initialise Class Using YAML config

        Parameters:
            cfg (str): Config file to load, default vendor_dict.yaml
        
        Raises:
            FileNotFoundError is yaml file is not found
        '''
        self.config = {}
   
        # Check for yaml file and raise exception if not found
        if os.path.isfile(cfg):
            # Read yaml configuration file
            try:
                self.config = yaml.safe_load(open(cfg, 'r'))
            except yaml.YAMLError as err:
                logging.error(err)
                raise
        else:
            logging.error(f'No such file {cfg}')
            raise FileNotFoundError(f'YAML config file "{cfg}" not found.')

        return


    def version(self):
        '''
        Returns:
        
            str containing config file version or 'Version not defined'
        '''
        if 'version' in self.config.keys():
            version = self.config['version']
        else:
            version = 'Version not defined'

        return version


    def keys(self):
        '''
        Returns:
            list of top level keys
        '''
        return self.config.keys()


    def vendors(self):
        '''
        Returns:
           list of defined vendors
        '''
        return self.config['vendors'].keys()


    def vendor_keys(self, vendor):
        '''
        Returns vendor top level keys

        Parameters:
            vendor (str): Vendor Identifier
        
        Returns:
            list of keys defined for a vendor
        '''
        if self.included(vendor):
             response = self.config['vendors'][vendor].keys()
        else:
            response = None
        
        return response


    def count(self):
        '''
        Get numbner of defined vendors
    
        Returns:
            int
        '''
        return len(self.config['vendors'])  


    def included(self, vendor):
        '''
        Check whether this vendor is configured

        Parameters:
            vendor (str): Vendor Identifier

        Returns bool
        '''
        status = False
        if vendor in self.vendors():
            status = True
        else:
            status = False

        return status


    def vendor_description(self, vendor):
        '''
        Get description of vendor

        Parameters:
            vendor (str): Vendor Identifier
        '''
        desc = None
        if self.included(vendor):
            desc = self.config['vendors'][vendor]['description']
        else:
            desc = None
        
        return desc


    def vendor_prefix(self, vendor):
        '''
        Get the prefix is present as a string

        Parameters:
            vendor (str): Vendor Identifier
        
        Returns:
            string containing defined prefix or '' if none
        '''
        prefix = ''
        if self.included(vendor):
            if 'prefix' in self.vendor_keys(vendor):
                prefix = self.config['vendors'][vendor]['prefix']
        
        return prefix


    def option_def(self, vendor):
        '''
        Returns option definition as dict

        Parameters:
            vendor (str): Vendor Identifier
        
        Returns:
            Dict containing both parent and sub option definitions
        '''
        opt_def = {}
        if self.included(vendor):
            if 'option-def' in self.vendor_keys(vendor):
                opt_def = self.config['vendors'][vendor]['option-def']
            else:
                logging.error(f'No option definition for vendor {vendor}')
        else:
            logging.error(f'Vendor: {vendor} not defined')
        
        return opt_def


    def parent_opt_def(self, vendor):
        '''
        Returns parent-option definition as dict

        Parameters:
            vendor (str): Vendor Identifier
        
        Returns:
            dict containing parent option definition
        '''
        opt_def = {}
        parent_def = {}
        if self.included(vendor):
            opt_def = self.option_def(vendor)
            if 'parent-option' in opt_def.keys():
                parent_def = opt_def['parent-option']
            else:
                logging.error(f'No parent-option for vendor {vendor}')
        else:
            logging.error(f'Vendor: {vendor} not defined')
        
        return parent_def


    def sub_options(self, vendor):
        '''
        Returns list of sub-option definitions

        Parameters:
            vendor (str): Vendor Identifier
        
        Returns:
            list of dict
        '''
        opt_def = {}
        sub_opt_defs = []
        if self.included(vendor):
            opt_def = self.option_def(vendor)
            if 'sub-options' in opt_def.keys():
                sub_opt_defs = opt_def['sub-options']
            else:
                logging.error(f'No parent-option for vendor {vendor}')
        else:
            logging.error(f'Vendor: {vendor} not defined')
        
        return sub_opt_defs
    
    
    def dump_vendor_def(self, vendor):
        '''
        Returns the vendor definition as a dict

        Parameters:
            vendor (str): Vendor Identifier
        
        Returns:
            dict containing vendor definition
        '''
        vendor_def = {}
        if self.included(vendor):
            vendor_def = self.config['vendors'][vendor]
        
        return vendor_def
