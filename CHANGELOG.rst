*********
ChangeLog
*********

|	20220929 	v0.8.13 Suppport direct use of api_key instead of inifile
|	20220901 	v0.8.12 Update to b1oph to support unknown app codes
|	20220323 	v0.8.11 Fix typo in b1tdc class
|	20220323 	v0.8.10 Add/delete items to custom list methods (b1tdc)
|	20220322 	v0.8.9  Publish recent changes
|	20220314 	v0.8.8 	Added custom list methods to b1tdc
|	20220309 	v0.8.8 	Added country/countryip methods to b1td class
|	20220224 	v0.8.7 	Fixed b1notifications class and doc update
|	20211217 	v0.8.6 	Udate documentation and PyPy release version no.
|	20211217 	v0.8.5 	Support list of sources for b1td.dossierquery()
|	20211204 	v0.8.4 	App control for OPHs
| 	20211102 	v0.8.3 	Added OPH status reporting methods
| 	20210805 	v0.8.2 	Improved error protection
| 	20210805 	v0.8.1 	Added requirements.txt for yaml
|	20210804 	v0.8.0 	Added output csv and yaml output
| 	20210804 	v0.7.9 	Minor bug fixes to dhcputils.py
| 	20210803 	v0.7.9 	Updates to b1ddi to support 'actions'
| 	20210730 	v0.7.8 	Minor bugs in new dhcp_decode class
| 	20210730  	v0.7.8 	dhcp_decode class
| 	20210726 	v0.7.6 	Documentation Updated for dhcp option classes
|	20210723 	v0.7.6 	Prefix handling in dhcputils, minor bug fixes
|	20210718 	v0.7.5 	dhcp_utils.py with near complete coding class
|   20210713	v0.7.4	Methods and docs for b1diagnostics class
|   20210709	v0.7.3	Added get_ophid() method to b1oph class
|   20210621	v0.7.2	Fixed issue with get_zone_child() method in b1ddi
|   20210618	v0.7.1	Framwork for b1diagnostics and b1notifications classes
|   20210308	v0.7.0	Added api_key format verification, raising exception
|   20210308	v0.6.9	Added exception raising for ini file not found
|   20210221	v0.6.8	Created 'public' generic methods for get, create, i
|                       replace, update:wq
|   20210215	v0.6.7	Added New Platform classes for new API elements
|                       b1anycast, b1authn, b1bootstrap, b1oph, b1sw, b1ztp
|                       Deprecating b1platform class (inherits b1oph for
|                       compatibility
|   20210212	v0.6.6	Added b1cdc class
|   20201105	v0.6.5	Minor bug fixes
|   20201105	v0.6.2	Added get_all_auditlog() method
|   20201105	v0.6.1	Dossier & threat enrichment methods added
|   20201102	v0.6.0	Fixed the add_tag and delete_tag methods
|   20201022	v0.5.9	Added auditlog method to b1platform
|   20200907	v0.5.8	Fixed a regex warning in utils.buildregex()
|   20200904	v0.5.7	Added get_option_ids helper method.
|   20200821	v0.5.5	Changes to project_urls for packaging
|   20200821	v0.5.4	Fixed fact that documentation wasn't included in 
|                       package.
|   20200818    v0.53   Streamlined get_id using _filter
|   20200818    v0.5.1  Initial Classes for Threat Defence DFP
|   20200818    v0.5.0  Initial Classes for Threat Defence (EP, Cloud, LAD)
|   20200817    v0.4.1  Added tag manipulation to b1ddi
|   20200810    v0.4.0  Minor changes and improved documentatin
|   20200810    v0.3.9  Fixed bug in b1td.get method
|   20200807    v0.3.8  Created b1td class for TIDE API b1td.py
|   20200714    v0.3.0  Added specific add/delete tags for on_prem_hosts
|   20200714    v0.2.4  Added create and update methods to b1platform class
|   20200713    v0.2.1  Renamed patch to update as originally intended 
|   20200713    v0.2.0  Removed original methods for get_object
|   20200713    v0.1.5  Added get_object_by_key and create initial documentation
|   20200711    v0.1.2  Added generic wrappers for DDI for create and delete
|                       Added get_id method to get object id from key/value pair
|   20200710    v0.1.1  Generic Wrapper and restructuring 
|   20200708    v0.0.5  Read only examples for several b1 objects
|		                Commit before restructuring to a more generic
|                       wrappers and useful functions
|   20200701    v0.0.2  Subclass for b1ddi api methods added to b1
|   20200629    v0.0.1  Initial Class commit for b1 class
|                       Base class attributes and ini file 
|                       handling.

