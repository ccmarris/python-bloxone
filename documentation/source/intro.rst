============
Introduction
============

This module forms the functional basis for the demo scripts that form part
of the Threat Intelligence toolkit whose aim is to provide demonstration scripts 
for BloxOne ThreatDefense. These can be used for API demonstrations, or help 
to simplify PoCs for Threat Intelligence, demonstrating the value of TIDE 
and our threat intel offerings.

The module simplifies some of the common TIDE and Dossier API calls, provides 
some useful data validation and normalisation functions. Functions are also 
included to use a local sqlite database containing local TIDE data generated [#]_

This documentation assumes that you have python3 installed and are familiar with 
both the Unix command line, files and the use of pip/pip3 to install any 
appropriate modules.


.. [#] Please see the :mod:`create-threat-intel-db.sh` tool for more details
