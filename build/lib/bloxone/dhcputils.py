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

 Date Last Updated: 20210804

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
__version__ = '0.2.7'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import logging
import ipaddress
import os
import yaml
import binascii
import bloxone
from pprint import pprint

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
            logging.error(f'{ip} not a valid IP')
            hex_value = ''

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
            no_octets = size // 4
            fmt = f'{{:0{no_octets}x}}'
            if i < 0 and abs(i) < max_size:
                hex_str = fmt.format(i + (2**size))
            elif i < max_size:
                hex_str = fmt.format(i)
            else:
                raise TypeError(f'{i} is out of range for uint{size} type')

        return hex_str 


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
        if array:
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
        print('Data tests:')
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


# DHCP Decoding Utils

class dhcp_decode():
    '''
    Class to assist with Hex Encoding of 
    DHCP Options and sub_options
    '''
    def __init__(self) -> None:
        self.opt_types = [ 'string', 
                           'ip',
                           'array_of_ip',
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


    def hex_string_to_list(self, hex_string):
        '''
        Take a hex string and convert in to a list

        Parameters:
            hex_string (str): Hex represented as string

        Returns:
            list of hex bytes
        '''
        hex_list = []
        
        # Remove colons if present
        hex_string = hex_string.replace(':','')

        # Turn hex_string into a list
        for h in range(0, len(hex_string), 2):
            hex_list.append(hex_string[h:h+2])

        return hex_list

    def hex_to_suboptions(self, hex_string, encapsulated=False):
        '''
        Extract the sub-options from the hex data 
        '''
        hex_list = []
        index = 0
        subopt = {}
        suboptions = []
        opt_len = 0
        opt_data = ''
        opt_code = ''

        # Turn hex_string into a list
        hex_list = self.hex_string_to_list(hex_string)
            
        # If encapsulated assume first two bytes
        if encapsulated:
            index = 2

        while index <= (len(hex_list) - 2 ):
            opt_code = hex_list[index]
            opt_len = int(hex_list[index+1], 16)
            # Get option data
            for i in range(index + 2, (index + opt_len + 2)):
                if i >= len(hex_list):
                    logging.error(f'Data encoding error, non-standard format')
                    break    
                else:
                    opt_data += hex_list[i]
            
            # Build sub_opt and add to list of suboptions
            sub_opt = { 'code': self.hex_to_optcode(opt_code),
                        'data_length': opt_len,
                        'data': opt_data }
            
            suboptions.append(sub_opt)

            # Reset opt_data
            opt_data = ''

            # Move index 
            index = index + opt_len + 2
        
        return suboptions


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
    def hex_to_ip(self, hex_string):
        '''
        Decode a 4 or 16 octect hex string to an IPv4 or IPv6 string 

        Parameters:
            hex_string (str): Hex representation of an IPv4 or IPv6 address 
        
        Returns:
            IP Address as a string
        '''
        ip = ''
        hex_string = hex_string.replace(':','')
        no_of_octects = self.hex_length(hex_string) 

        # Check number of octets
        if no_of_octects == '04' or no_of_octects == '10':
            # Assume IPv4 or IPv6
            int_ip = int(hex_string, 16)
            if self.validate_ip(int_ip):
                ip = ipaddress.ip_address(int_ip).exploded
            else:
                logging.error(f'{hex_string} not a valid IP Address')
                ip = ''
        else:
            ip = ''

        return ip

    def hex_to_array_of_ip(self, hex_string):
        '''
        Decode array of IPv4 or IPv6 addresses to CSV string 

        Parameters:
            hex_string (str): Hex representation of an array of IPv4 or IPv6
        
        Returns:
            IP Addresses in a CSV string
        
        '''
        array_of_ip = ''
        
        hex_length = int(self.hex_length(hex_string),16)

        if hex_length in [ 8, 12, 16, 20, 24 ]:
            # Assume IPv4
            for ip in [hex_string[n:n+8] for n in range(0, len(hex_string), 8)]:
                dip = self.hex_to_ip(ip)
                array_of_ip += dip + ','
            
        elif hex_length in [ 32, 48, 64 ]:
            # Assume IPv6
            for ip in [hex_string[n:n+32] for n in range(0, len(hex_string), 32)]:
                dip = self.hex_to_ip(ip)
                array_of_ip += dip + ','

        else:
            array_of_ip = 'array_of_ip_failed.'
            
        array_of_ip = array_of_ip[:-1]
            
        return array_of_ip


    # Methods for IPv4 and IPv6
    def hex_to_ipv4_address(self, hex_string):
        '''
        Decode a hex string to an IPv4 Address as a string

        Parameters:
            hex_string (str): Hex representation of an IPv4 address 
        
        Returns:
            IPv4 Address as a string
        '''
        hex_string = hex_string.replace(':','')
        return self.hex_to_ip(hex_string)
        
    
    def hex_to_ipv6_address(self, hex_string):
        '''
        Decode a hex string to an IPv6 address as a string 

        Parameters:
            hex_string (str): Hex representation of an IPv6 address 
        
        Returns:
            IPv6 Address as a string
        '''
        hex_string = hex_string.replace(':','')
        return self.hex_to_ip(hex_string)


    # String/text encoding
    def hex_to_string(self, hex_string):
        '''
        Decode a string of hex values to a text string

        Parameters:
            hex_string (str): Hex representation of a string
        
        Returns:
            text string (str)
        '''
        hex_string = hex_string.replace(':','')
        s = binascii.unhexlify(hex_string).decode()
        return s


    # Boolean encoding
    def hex_to_boolean(self, hex_string):
        ''' 
        Decode Hex value as a string to 'true' or 'false'

        Parameters:
            hex_string (str): Hex value as a str
        
        Returns:
           string representation of a boolean
        '''
        hex_string = hex_string.replace(':','')

        # Assume true if not zero i.e. check all bits for non-zero
        if int(hex_string, 16) == 0:
            text_bool = 'False'
        else:
            text_bool = 'True'
        
        return text_bool


   # integer encodings 
    def hex_to_int(self, hex_string, size=8):
        '''
        Decode hex to signed integer of defined size

        Parameters:
            hex_string (str): hex value as string
            size (int): size in bits [8, 16, 32]
        
        Returns:
            integer
        '''
        value = 0
        i_sizes = [ 8, 16, 32 ]
        hex_string = hex_string.replace(':','')

        i = int(hex_string, 16)
        if size in i_sizes:
            max_bits = size - 1
            if i < (2**size):
                if (i > (2**max_bits)):
                    value = -abs(i - (2**max_bits))
                else:
                    value = i
            else:
                raise ValueError(f'{i} is out of range for int{size} type')
        else:
            raise ValueError(f'Size must be 8, 16, or 32')

        return value 


    def hex_to_uint(self, hex_string, size=8):
        '''
        Encode integer of specified size as unsigned int in hex
        Uses 2's compliment if supplied with negative number


        Parameters:
            i (int): integer value to encode
            size (int): size in bits [8, 16, 32]
        
        Returns:
            hex encoding as string
        '''
        i_sizes = [ 8, 16, 32 ]
        hex_string = hex_string.replace(':','')
        i = int(hex_string, 16)

        if size in i_sizes:
            max_size = 2**size
            if i < max_size:
                value = i
            else:
                raise ValueError(f'{i} is out of range for uint{size} type')
        else:
            raise ValueError(f'Size must be 8, 16, or 32')

        return value 


    # Methods for intX and uintX
    def hex_to_int8(self, value):
        return self.hex_to_int(value, size=8)


    def hex_to_uint8(self, value):
        return self.hex_to_uint(value, size=8)


    def hex_to_int16(self, value):
        return self.hex_to_int(value, size=16)


    def hex_to_uint16(self, value):
        return self.hex_to_uint(value, size=16)


    def hex_to_int32(self, value):
        return self.hex_to_int(value, size=32)


    def hex_to_uint32(self, value):
        return self.hex_to_uint(value, size=32)


    # FDQN Encoding
    def hex_to_fqdn(self, hex_string):
        '''
        Decode RFC 1035 Section 3.1 formatted hexa to fqdn

        Parameters:
            hex_string (str): hex encoded fqdn

        Returns:
            fqdn as string
        '''
        hex_list = []
        index = 0
        fqdn = ''
        label_len = 0
        label = ''

        # Turn hex_string into a list
        hex_list = self.hex_string_to_list(hex_string)
            
        label_len = int(hex_list[index], 16)
        while label_len != 0:
            
            # Build label
            for i in range(index + 1, (index + label_len + 1)):
                label += hex_list[i]
            
            # Build fqdn and reset label
            fqdn += self.hex_to_string(label) + '.'
            label = ''

            # Reset index and check
            index = index + label_len + 1
            if index < len(hex_list):
                label_len = int(hex_list[index], 16)
            else:
                logging.warning('Reach end before null')
                label_len = 00

        return fqdn


    # Binary Encoding
    def hex_to_binary(self, data):
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
        else:
            hex_string = data.replace(':','')

        # Force hex encoding without 0x using base
        hex_value = '{:02x}'.format(int(data, base))

        return hex_value

    
    # Empty Encoding
    def hex_to_empty(self, data):
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
    def hex_to_optcode(self, hex_string):
        '''
        Encode Option Code in hex (1-octet)

        Parameters:
            optcode (str/int): Option Code 
        
        Returns:
            hex encoding as string
        '''
        opt_code = self.hex_to_int8(hex_string)
        return opt_code


    def hex_length(self, hex_string):
        '''
        Encode Option Length in hex (1-octet)

        Parameters:
            hex_string (str): Octet Encoded Hex String
        
        Returns:
            Number of Hex Octects as hex encoded string
        '''
        hex_string = hex_string.replace(':','')
        hex_len = '{:02x}'.format(int(len(hex_string) / 2))
        return hex_len


    def check_data_type(self, optcode, sub_defs=[]):
        '''
        Get data_type for optcode from sub optino definitions

        Parameters:
            optcode (int): Option code to check
            sub_defs (list of dict): sub option definitions to cross
                    reference
        
        Returns:
            data_type as str
        
        '''
        data_type = ''

        if sub_defs:
            for d in sub_defs:
                if int(optcode) == int(d['code']):
                    data_type = d['type']
                    # Check for array_of_ip 
                    if 'array' in d.keys():
                        if ('ip' in data_type) and d['array']:
                            data_type = 'array_of_ip'
                    break
        
        return data_type
 

    def get_name(self, optcode, sub_defs=[]):
        '''
        Get data_type for optcode from sub optino definitions

        Parameters:
            optcode (int): Option code to check
            sub_defs (list of dict): sub option definitions to cross
                    reference
        
        Returns:
            name as str
        
        '''
        name = ''

        if sub_defs:
            for d in sub_defs:
                if optcode == d['code']:
                    name = d['name']
                    break
        
        return name
                            

    def guess_data_type(self, subopt, padding=False):
        '''
        '''
        data_type = ''
        data_types = []
        dl = subopt['data_length']
        data = subopt['data'].replace(':','')

        # Check for 1 byte first
        if dl == 1:
            # int8 or bool (so treat as int8)
            # data_types.append('int8')
            data_type = 'int8'
        else:
            # We know it has more than one byte
                
            if data[-2:] == '00' and not padding: 
                # Possible FQDN
                logging.debug('Checking fqdn guess')
                fqdn = self.hex_to_fqdn(subopt['data'])
                # Validate FQDN
                if bloxone.utils.validate_fqdn(fqdn, self.fqdn_re):
                    logging.debug('FQDN verified')
                    data_types.append('fqdn')
                    data_type = 'fqdn'

            if dl in [4, 16]:
                logging.debug('CHecking for type ip')
                if self.hex_to_ip(data):
                    data_types.append('ip')
                    data_type = 'ip'

            if dl in [8, 32]:
                logging.debug('Checking for array of ip')
                if self.hex_to_ip(data[:dl]):
                    data_types.append('ip')
                    data_type = 'array_of_ip'
            
            if data_type == '':
                logging.debug('Default guess of string')
                data_type = 'string'            


        return data_type
        
    
    def decode_data(self, data, data_type='string', 
                    padding=False,
                    pad_bytes=1,
                    array=False):
        '''
        '''
        decoded = ''
        if data_type in self.opt_types:
            if 'ip' in data_type and array:
                data_type = 'array_of_ip'
            hex_to_type = eval('self.' + 'hex_to_' + data_type)
        else:
            logging.error(f'Unsupported Option Type {data_type}')
            logging.info('Unsupported option type, ' +
                         'attempting to process as string')
            hex_to_type = eval('self.hex_to_string')
        
        decoded = hex_to_type(data)

        return decoded
        

    def decode_dhcp_option(self, 
                           hex_string,
                           sub_opt_defs=[],
                           padding=False,
                           pad_bytes=1,
                           encapsulated=False,
                           id=None,
                           prefix=''):
        '''
        Attempt to decode DHCP options from hex representation

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
        value = ''
        str_value = ''
        suboptions = []
        de_sub_opt = {}
        decoded_opts = []
        parent = {}
        guessed = False
        hex_string = hex_string.replace(':','')

        if (len(hex_string) % 2) == 0:
            if encapsulated:
                parent_opt = self.hex_to_opcode(hexstring[:2])
                total_len = self.hex_to_int8(hexstring[2:4])
                hex_string = hex_string[4:]
                parent = {'parent': parent_opt, 'total_len': total_len }
                decoded_opts.append(parent)

            # Break out sub-options
            suboptions = self.hex_to_suboptions(hex_string)

            # Attempt to decode sub_options
            for opt in suboptions:
                if sub_opt_defs:
                    data_type = self.check_data_type(opt['code'],
                                                    sub_defs=sub_opt_defs)
                    name = self.get_name(opt['code'], sub_defs=sub_opt_defs)

                else:
                    logging.debug(f'Attempting to guess option type for {opt}')
                    data_type = self.guess_data_type(opt)
                    guessed = True
                    name = 'Undefined'
                
                if data_type: 
                    value = self.decode_data(opt['data'], data_type=data_type)
                
                str_value = self.decode_data(opt['data'], data_type='string')

                de_sub_opt = { 'name': name,
                            'code': opt['code'],
                            'type': data_type,
                            'data_length': opt['data_length'],
                            'data': value,
                            'data_str': str_value,
                            'guess': guessed }

                decoded_opts.append(de_sub_opt)
        else:
            logging.error('Hex string contains incomplete octets')

        return decoded_opts


    def output_decoded_options(self, decoded_opts=[], output='pprint'):
        '''
        Simple output for decode_dhcp_options() data

        Parameters:
            decoded_opts (list): List of dict
            output (str): specify format [pprint, csv, yaml]
        
        '''
        formats = [ 'csv', 'pprint', 'yaml']
        header = ''
        head_printed = False
        line = ''
        
        if len(decoded_opts):
            if output in formats:
                # Output simply with pprint
                if output == 'pprint':
                    pprint(decoded_opts)
                # Output to CSV
                if output == 'csv':
                    for item in decoded_opts: 
                        if 'parent' in item.keys():
                            header = 'Parent, Total Length'
                            pprint(header)
                            pprint(f'{item["parent"]}, ' +
                                  f'{item["total_len"]}')
                        elif not head_printed:
                            header = ''
                            for key in item.keys():
                                header += key + ','
                            header = header[:-1]

                            pprint(header)
                            head_printed = True
                        else:
                            for key in item.keys():
                                line += repr(item[key]) + ','
                            line += line[:-1]
                            pprint(line)
                            line = ''
                # Output to normalised YAML
                if output == 'yaml':
                    try:
                        y = yaml.safe_dump(decoded_opts)
                        print(y)
                    except:
                        print('Could not convert to yaml')

            else:
                print(f'{output} not supported for output')
                print(f'Suported formats include: {formats}')
                print(decoded_opts)
        else:
            print('No option data')
        
        return
        
        
    def tests(self):
        '''
        Run through encoding methods and output example results
        '''
        encode = bloxone.dhcp_encode()
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

        print(f'Decoding types supported: {self.opt_types}')
        print()
        print('Non-array tests:')
        for data_test in test_data:
            enc_str = encode.encode_data(data_test)
            if 'array' in data_test.keys():
                array = data_test['array']
            else:
                array=False

            dec_str = self.decode_data(enc_str, 
                                       data_type=data_test['type'],
                                       array=array)
            print(f'Type: {data_test["type"]}, Hex: {enc_str}, ' +
                  f'Decoded: {dec_str}, Original: {data_test["data"]}')
        
        print()
        # Padding Test
        # test_data = { 'code': '99', 'type': 'string', 'data': 'AABBCCDD' }
        # result = encode.encode_data(test_data, padding=True)
       #  print(f'Padding test (1 byte), type string: {test_data["data"]}' +
        #       f' {result}')
        # Full encode test
        test_data = [ { 'code': '1', 'type': 'string',
                        'data': 'AABBDDCCEEDD-aabbccddeeff' },
                      { 'code': '2', 'type': 'ipv4_address',
                        'data': '10.10.10.10' },
                      { 'code': '3', 'type': 'ipv4_address',
                        'data': '10.10.10.10,11.11.11.11', 'array': True },
                      { 'code': '4', 'type': 'boolean', 'data': True },
                      { 'code': '5', 'type': 'int8', 'data': '22' } ]
        result = encode.encode_dhcp_option(test_data)
        print(f'Full encoding of sample Hex: {result}')
        decode = self.decode_dhcp_option(result, sub_opt_defs=test_data)
        print(f'Decoding result:')
        self.output_decoded_options(decode)

        return