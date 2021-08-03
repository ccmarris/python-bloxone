=========================================
Usage and Examples for dhcputils (encode)
=========================================

The DHCP Utils provides classes to assist with the encoding and decoding of
DHCP options in to/from hexidecimal. The primary use case is for sub-option
encoding for custom option spaces, in particular, Option 43 encoding.


Encoding Class
--------------

The :class:`bloxone.dhcp_encode()` class provides a set of *encode* methods
to enable the encoding of defined DHCP sub options and data. 

To encode the specific data-types a set of *type_to_hex* methods are provided.
These will take a specific input data=type and apply the required encoding
methodology to generate a compliant hexidecimal string for


Usage
-----

The core aim of the class is to provide a simpler interface to encode DHCP sub
options defined as a dictionary and provide an encoding.

To ensure flexibility the encoding is broken down in to three methods:
:func:`encode_dhcp_option()`, :func:`encode_sub_option()` and
:func:`encode_data()`. 

Sub-options are defined as a dictionary, with three required keys:

	'code' 
		the sub option code
	'type'
		the data-type
	'data'
		the data to encode using the specified type

And several optional keys:

	'array'
		Boolean to indicate whether the data should be encoded as
		an array, e.g. array of IP addresses
	'data-only'
		Boolen to indicate that only the data in the sub option should
		be encoded. i.e. do not add the encoded option code and length
	
	
For example::

	sub1 = { 'code': 1, 'type': 'string', 'data': 'ABCDEFG'}
	sub2 = { 'code': 2, 'type': 'ipv4_address', 
		 'data': '10.10.10.10,10.11.11.11', 'array': True }


Since there is typically more that one sub-option required, these can be added
to a list that is processed, and encoded, by the :func:`encode_dhcp_option()`
method::

	options = [ sub1, sub2 ]


An example, with example output is shown below::

	import bloxone

	de = bloxone.dhcp_encode()

	# Set up the sub-options
	sub1 = { 'code': 1, 'type': 'string', 'data': 'ABCDEFG'}
	sub2 = { 'code': 2, 'type': 'ipv4_address', 
		 'data': '10.10.10.10,10.11.11.11', 'array': True }
		 
	# Create list for option to be encoded together
	options = [ sub1, sub2 ]

	# Encode e.g. for Option 43
	h = de.encode_dhcp_option(options)
	print(h)
	
	'''
	>>> print(h)
	01074142434445464702080a0a0a0a0a0b0b0b
	'''

	# Show the encoding for just one sub-option
	print(de.encode_sub_option(sub2))

	'''
	>>> print(de.encode_sub_option(sub2))
	02080a0a0a0a0a0b0b0b
	'''

	test_data = { 'code': '101', 'type': 'fqdn', 'data': 'www.example.com' }
	hex_data = encode_data(test_data)

	'''
	>>> print(de.encode_data(test_data))
	03777777076578616d706c6503636f6d00
	'''


Return a list of supported data types::

	>>> import bloxone
	>>> de = bloxone.dhcp_encode()
	>>> de.opt_types
	['string', 'ipv4_address', 'ipv6_address', 'boolean', 'int8', 'uint8',
	 'int16', 'uint16', 'int32', 'uint32', 'fqdn', 'binary', 'empty']


Each of the supported data-types has a specific method of the format
*type_to_hex()*. These can be directly access and typically support data both
in its native format and as a string::

	de.string_to_hex('Hello World')
	de.ip4_address_to_hex('192.168.1.101')
	de.fqdn_to_hex('www.infoblox.com')
	de.int8_to_hex('22') or int8_to_hex(22)

	etc


Specific functions to return the length of the hexidecimal string in hex and
encoding of the option code (basically a wrapper of int8), are also provided::

	h = de.ip4_address_to_hex('10.10.10.10')
	de.hex_length(h)
	de.optcode_to_hex(125)


A :func:`tests()` method is also provided that will show example encodings 
for each data-type and option encodings::

	>>>de.tests()
	Encoding types supported: ['string', 'ipv4_address', 'ipv6_address', 'boolean', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'fqdn', 'binary', 'empty']

	Non-array tests:
	Type: string: AABBDDCCEEDD-aabbccddeeff, Encoded: 4141424244444343454544442d616162626363646465656666, Length(hex): 19
	Type: ipv4_address: 10.10.10.10, Encoded: 0a0a0a0a, Length(hex): 04
	Type: ipv4_address: 10.10.10.10,11.11.11.11, Encoded: 0a0a0a0a0b0b0b0b, Length(hex): 08
	Type: boolean: True, Encoded: 01, Length(hex): 01
	Type: int8: 22, Encoded: 16, Length(hex): 01
	Type: int8: -22, Encoded: 96, Length(hex): 01
	Type: uint8: 22, Encoded: 116, Length(hex): 01
	Type: int16: 33, Encoded: 0021, Length(hex): 02
	Type: int16: 33, Encoded: 0021, Length(hex): 02
	Type: uint16: 33, Encoded: 10021, Length(hex): 02
	Type: int32: 44, Encoded: 0000002c, Length(hex): 04
	Type: uint32: -44, Encoded: ffffffd4, Length(hex): 04
	Type: uint32: 44, Encoded: 10000002c, Length(hex): 04
	Type: fqdn: www.infoblox.com, Encoded: 0377777708696e666f626c6f7803636f6d00, Length(hex): 12
	Type: binary: DEADBEEF, Encoded: deadbeef, Length(hex): 04
	Type: empty: , Encoded: , Length(hex): 00
	Type: ipv6_address: 2001:DB8::1, Encoded: 20010db8000000000000000000000001, Length(hex): 10
	Type: ipv6_address: 2001:DB8::1,2001:DB8::2, Encoded: 20010db800000000000000000000000120010db8000000000000000000000002, Length(hex): 20

	Padding test (1 byte), type string: AABBCCDD 414142424343444400
	Full encoding of sample: 01194141424244444343454544442d61616262636364646565666602040a0a0a0a03080a0a0a0a0b0b0b0b040101050116
	>>> 


