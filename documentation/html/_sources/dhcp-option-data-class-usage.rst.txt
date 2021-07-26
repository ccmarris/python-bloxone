=============================
DHCP Options Data Class Usage
=============================

To simplify the definition and encoding/decoding of DHCP Options with the
:class:`bloxone.dhcp_encode()` class, a data class to handle Vendor definitions
is included.  

The :class:`bloxone.DHCP_OPTION_DEFS()` class provides a simple interface to
read the vendor definition from a YAML file that can contain one or more
vendor definitions.

YAML File Format
----------------

The base file definition allows for a file version number and a list of 
vendors, a sample showing all of the options is shown below::

    ---
    # DHCP Vendor Option Definitions
    version: 0.0.1

    vendors:

        Sample-Vendor:
            vci: sample-vci
            description: My Vendor Class
            prefix: "<prefix str if required>"
            option-def: 
                parent-option:
                    name: option name
                    code: 43
                    type: binary
                    array: False
                sub-options:
                    - name: Sub Opt 1
                        code: 1
                        type: string
                        data: Encode this string
                        array: False
                        data-only: False
                    - name: Sub Opt 2
                        code: 5
                        type: ipv4_address
                        data: 10.10.10.10,20.20.20.20
                        array: True
                        data-only: False

The format allows the complete definition of a vendor, with the core element
being the *option-def* that defines, in particular, the list of sub-options
for encoding.

The definition can include a prefix to prepend to the encoding, and data-only
flags to handle both option 43 style encodings and option 125 style encodings.

Example Definitions::

    ---
    # DHCP Vendor Option Definitions
    version: 0.0.1

    vendors:

        MS-UC-Client:
            vci: MS-UC-Client
            description: Microsoft Lync Client
            option-def:
                parent-option:
                    name: option 43
                    code: 43
                    type: binary
                    array: False
                sub-options:
                    - name: UC Identifier
                        code: 1
                        type: string
                        data: MS-UC-Client
                        array: False
                    - name: URL Scheme
                        code: 2
                        type: string
                        data: https
                        array: False
                    - name: Web Server FQDN
                        code: 3
                        type: string
                        data: epslync01.epsilonhq.local
                        array: False
                    - name: Web Server Port
                        code: 4
                        type: string
                        data: 443
                        array: False
                    - name: Certificate Web Service
                        code: 5
                        type: string
                        data: /CertProv/CertProvisioningService.svc
                        array: False


        ####### CISCO
        # Option 43 sub-option 241

        Cisco AP:
            vci: Cisco AP
            description: Cisco Aironet Series APs
            option-def:
                parent-option:
                    name: option 43
                    code: 43
                    type: binary
                    array: False
                sub-options:
                    - name: Controller IP
                        code: 241
                        type: ipv4_address
                        data: 10.150.1.15,10.150.50.15
                        array: True


        ####### MITEL

        Mitel:
            vci: Mitel
            description: Mitel Phone (prepend 00000403)
            prefix: "00000403"
            option-def:
                parent-option:
                    name: option 125
                    code: 125
                    type: binary
                    array: False
                sub-options:
                    - code: 125
                        type: string
                        data: id:ipphone.mitel.com;call_srv=X;vlan=X;dscp=46;l2p=X;sw_tftp=X
                        data-only: True


The :class:`bloxone.DHCP_OPTION_DEFS()` class allows you to specify the YAML
file to read, and enables you to read the elements quickly and easily. As 
an example, the file above can be used to encode the vendors sub-options::

    import bloxone
    de = bloxone.dhcp_encode()
    vendors = bloxone.DHCP_OPTION_DEFS('vendor_dict.yaml')
    if vendors.included('MS-US-Client'):
        print(de.encode_dhcp_option(vendors.sub_options('MS-US-Client')))
    
    '''
    Vendor: MS-UC-Client, Encoding: 010c4d532d55432d436c69656e7402056874
    74707303196570736c796e6330312e657073696c6f6e68712e6c6f63616c04033434
    3305252f4365727450726f762f4365727450726f766973696f6e696e675365727669
    63652e737663
    '''

    if vendors.included('Mitel'):
        print(de.encode_dhcp_option(vendors.sub_options('Mitel')))
    '''
    Vendor: Mitel, Encoding: 0000040369643a697070686f6e652e6d6974656c2e636f
    6d3b63616c6c5f7372763d583b766c616e3d583b647363703d34363b6c32703d583b737
    75f746674703d58
    '''

    # Process all vendors:
    for vendor in vendors.vendors():
        print(vendor)
        print(de.encode_dhcp_option(vendors.sub_options('Mitel')))


An example script using both classes to perform encodings from a CLI
can be found on github
https://github.com/ccmarris/dhcp_option_encoding


