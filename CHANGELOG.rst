*********
ChangeLog
*********

|  20200605    v2.60   Added get_domain, strip_host, and count_labels functions
|  20200529    v2.53   Made read_tide_ini generic returning dict of ini parameters 
|  20200508    v2.50   Added read_tide_ini() function to get api_key from ini
|                      Docstrings now consistent
|  20200504    v2.42   Updated normalise function for optional itype
|  20200501    v2.40   Added domain function to return two label domain
|                      from fqdn or fqdn if number of labels <= 2
|                      Standardised function docstrings
|  20200418    v2.30   Added functions for url conversion and
|                      data normalisation
|  20190625    v2.21   PEP8 Clean-up
|  20190605    v2.2    Added threatproperty to tideactivefeed function
|  20190104    v2.1    Changed to Simplified BSD license
|  20181122    v2.0    Added functions to get threat classes, properties
|                      and stats
|  20181112    v1.6    Bug fixes for offline database (import os)
|  20181112    v1.5    Switched to logging, removed hard exit()s on exceptions
|  20180619    v1.1    Cleaned up comments and self pydoc
|  20180614    v1.0    Added requests exception handling
|  20180614    v0.9    Moved querytideactive to querytidestate and
|                      Created new querytideactive to use expiration field
|  20180613    v0.8    Added local database functions (sqllite)
|  20180502    v0.7    Added target type for dossier query
|  20180501    v0.6    Added basic dossier query function
|  20180501    v0.5    Added call for TIDE Active Datafeed
|  20180430    v0.3    Added basic tide queries for a specific IOC
|  20180424    v0.1    Initial test library collection including data types
