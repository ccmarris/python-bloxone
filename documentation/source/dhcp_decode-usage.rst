=========================================
Usage and Examples for dhcputils (decode)
=========================================

The DHCP Utils provides classes to assist with the encoding and decoding of
DHCP options in to/from hexidecimal. The primary use case is for sub-option
encoding for custom option spaces, in particular, Option 43 encoding.


Decoding Class
--------------

The :class:`bloxone.dhcp_decode()` class provides a set of *decode* methods
to attempt to decode a hexideciaml string representation of DHCP sub-options.

To decode specific data-types a set of *hex_to_type* methods are provided.
These take a hexideciaml string representation of the data and apply the
required decoding methodology and return the decoded data.

Since and encoded set of DHCP sub-options does not include the data type
accurate decoding is problematic. Two mechanisms are provided to try and 
address this::
	
 	- It is possible to provide a known definition for the sub-options and 
	use the specified data types.

	- Allow the class to make a best-efforts *guess* of the data_type.

In both cases a string decoding is also applied and provided back. A flag,
*guess* is used to inform whether or not the data_type was *guessed* or 
based on a known definition.

The :class:`DHCP_OPTION_DEFS` class can be utilised to extract sub-option
definitions from a YAML configuration and maintain a vendor database of 
option definitions.


Usage
-----

The core aim of the class is to provide a simpler interface to decode DHCP sub
options and return this as a list of dictionary definitions detailing the 
decoding.

To ensure flexibility the decoding is broken down in to two methods:
:func:`decode_dhcp_option()` and :func:`decode_data()`. 

:func:`decode_data()` takes the hexideciaml string and a data_type and will
apply the appropriate hex_to_type() decoding method. For example::

	import bloxone
	de = bloxone.dhcp_decode()
	de.decode_data('0a0a0a0a', data_type='ipv4_address')
	# Output: '10.10.10.10'

	# Note this can be shortened to 
	# de.decode_data('0a0a0a0a', data_type='ip')


:func:`decode_dhcp_option` also takes a hexidecimal string, however, in this
case it will be enterpreted as an encoded set of sub-options (based on option
43 encoding). As mentioned due to the fact that this does not contain data
type information, you can either provide a dictionary containing an option
definition (of the same format used by the :class:`dhcp_encode()` class), 
or let the function attempt to make a guess. In both cases the string decoding
will be included in the response.

The method returns a list of decoded sub-options with a dictionary per sub 
option. This will be of the format::

	[ {'name': 'Undefined',
	   'code': 3,
  	   'data': '10.10.10.10,11.11.11.11',
       'data_length': 8,
  	   'data_str': '\n\n\n\n\x0b\x0b\x0b\x0b',
  	   'guess': True,
  	   'type': 'array_of_ip'} ]


For simple output an :func:`output_decoded_options` method is provided.

Examples::

	import bloxone
	de = bloxone.dhcp_decode()

	# Hex string to attempt to decode
	h = '01194141424244444343454544442d61616262636364646565666602040a0a0a0a' +
		'03080a0a0a0a0b0b0b0b040101050116'

	opt_list = de.decode_dhcp_option(h)
	de.output_decoded_options(opt_list)


This will produce the output::

	[{'code': 1,
	'data': 'AABBDDCCEEDD-aabbccddeeff',
	'data_length': 25,
	'data_str': 'AABBDDCCEEDD-aabbccddeeff',
	'guess': True,
	'name': 'Undefined',
	'type': 'string'},
	{'code': 2,
	'data': '10.10.10.10',
	'data_length': 4,
	'data_str': '\n\n\n\n',
	'guess': True,
	'name': 'Undefined',
	'type': 'ip'},
	{'code': 3,
	'data': '10.10.10.10,11.11.11.11',
	'data_length': 8,
	'data_str': '\n\n\n\n\x0b\x0b\x0b\x0b',
	'guess': True,
	'name': 'Undefined',
	'type': 'array_of_ip'},
	{'code': 4,
	'data': 1,
	'data_length': 1,
	'data_str': '\x01',
	'guess': True,
	'name': 'Undefined',
	'type': 'int8'},
	{'code': 5,
	'data': 22,
	'data_length': 1,
	'data_str': '\x16',
	'guess': True,
	'name': 'Undefined',
	'type': 'int8'}]

Example providing sub-option definitions using the same hex string::

	# Set up the sub-option definitions
	sub1 = { 'name': 'Test1', 'code': 1, 'type': 'string', 'data': ''}
	sub2 = { 'name': 'Test2', 'code': 2, 'type': 'ipv4_address', 
			'data': '', 'array': False }
	sub3 = { 'name': 'Test3', 'code': 3, 'type': 'ipv4_address',
			'data': '', 'array': True }
	sub4 = { 'name': 'Test4', 'code': 4, 'type': 'boolean' }
	sub5 = { 'name': 'Test5', 'code': 5, 'type': 'int8' }		 

	# Create list of option definitions
	options = [ sub1, sub2, sub3, sub4, sub5 ]

	opt_list = de.decode_dhcp_option(h, sub_opt_defs=options)
	de.output_decoded_options(opt_list)
	

Here you can see that the name and data-types are defined from sub-option
definitions::

	[{'code': 1,
	'data': 'AABBDDCCEEDD-aabbccddeeff',
	'data_length': 25,
	'data_str': 'AABBDDCCEEDD-aabbccddeeff',
	'guess': False,
	'name': 'Test1',
	'type': 'string'},
	{'code': 2,
	'data': '10.10.10.10',
	'data_length': 4,
	'data_str': '\n\n\n\n',
	'guess': False,
	'name': 'Test2',
	'type': 'ipv4_address'},
	{'code': 3,
	'data': '10.10.10.10,11.11.11.11',
	'data_length': 8,
	'data_str': '\n\n\n\n\x0b\x0b\x0b\x0b',
	'guess': False,
	'name': 'Test3',
	'type': 'array_of_ip'},
	{'code': 4,
	'data': 'true',
	'data_length': 1,
	'data_str': '\x01',
	'guess': False,
	'name': 'Test4',
	'type': 'boolean'},
	{'code': 5,
	'data': 22,
	'data_length': 1,
	'data_str': '\x16',
	'guess': False,
	'name': 'Test5',
	'type': 'int8'}]


As mentioned the :class:`DHCP_OPTION_DEFS` class can be utilised to access
vendor DHCP Option definitions from a YAML configuration an example script
and example vendor configuration file can be found as part of the 
`dhcp_option_encoding`_ project on GitHub. 

.. _dhcp_option_encoding: https://github.com/ccmarris/dhcp_option_encoding

A simple example using showing this is shown below::

	h = '010c4d532d55432d436c69656e740205687474707303196570736c' +
		'796e6330312e657073696c6f6e68712e6c6f63616c040334343305' + 
		'252f4365727450726f762f4365727450726f766973696f6e696e67' +
		'536572766963652e737663'
	v = bloxone.DHCP_OPTION_DEFS('vendor_dict.yaml')
	sub_options = v.sub_options('MS-UC-Client')

	opt_list = de.decode_dhcp_option(h, sub_opt_defs=sub_options)
	de.output_decoded_options(opt_list)


As with the :class:`dhcp_encode()` class you can get a list of supported 
decoding data types using the *opt_types** attribute::

	>>> import bloxone
	>>> de = bloxone.dhcp_decode()
	>>> de.opt_types
	['string', 'ip', 'array_of_ip', 'ipv4_address', 'ipv6_address', 'boolean', 
	'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'fqdn', 'binary', 
	'empty']

For decoding purposes the generic *ip* and *array_of_ip* types are exposed,
the respective methods support both IPv4 and IPv6.

Each of the supported data-types has a specific method of the format
*hex_to_type()*. These can be directly access and typically support data both
in its native format and as a string::

	de.hex_to_string('48656c6c6f20776f726c64')
	# 'Hello world'
	de.hex_to_ip('c0a80165')
	# '192.168.1.101'
	de.hex_to_fqdn('0377777708696e666f626c6f7803636f6d00')
	# 'www.infoblox.com.'
	de.hex_to_int8('16')
	# 22

	etc

A :func:`tests()` method is also provided that will show example 
encodings/decodings for each data-type and option encodings.


