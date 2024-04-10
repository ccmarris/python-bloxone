#!/usr/local/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 BloxOne Threat Defense Enpoint API Wrapper Class and Helpers

 Author: Chris Marrison

 Date Last Updated: 20240201

 Todo:

 Copyright (c) 2020 - 2024 Chris Marrison / Infoblox

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
__version__ = '0.3.0'
__author__ = 'Chris Marrison/Krishna Vasudeva'
__author_email__ = 'chris@infoblox.com'

import bloxone
import logging
import csv
import sys

# ** Global Vars **

class b1tdlad(bloxone.b1td):

    # Generic Methods
    def get(self, objpath, **params):
        '''
        Generic get object wrapper for Threat Defense objects

        Parameters:
            objpath (str):  Swagger object path
            id (str):       Optional Object ID
        
        Returns:
            response object: Requests response object
        '''
        # Build url
        url = self.tdlad_url + objpath
        url = self._add_params(url, **params)
        logging.debug("URL: {}".format(url))

        response = self._apiget(url)

        return response


    def update(self, objpath, id="", body=""):
        '''
        Generic create object wrapper 

        Parameters:
            objpath (str):  Swagger object path
            body (str): JSON formatted data payload

        Returns:
            response object: Requests response object
        '''
        # Build url if needed
        url = self.tdlad_url + objpath
        url = self._use_obj_id(url, id=id)
        logging.debug("URL: {}".format(url))

        # Make API Call
        response = self._apiput(url, body)

        return response
    

    def get_lookalikes(self, target_domain='', **params):
        '''
        '''
        url = f'{self.tdlad_url}/lookalikes'

        if target_domain:
            filter = f'target_domain=="{target_domain}"'
            url = self._add_params(url, _filter=filter)
            url = self._add_params(url, first_param=False, **params)
        else:
            url = self._add_params(url, **params)
        
        response = self._apiget(url)
        
        return response
    

    def lookalike_to_csv(self, records, file=sys.stdout, enriched=False):
        '''
        Output lookalike data to CSV

        Parameters:
            records (list): Lookalike API result data
            file (filehandler): File opened for write with newline=''
            enriched (bool): Enhance data using dossier
        '''
        lookalikes = records.get('results')
        if not lookalikes:
            lookalikes = records
        
        if lookalikes:
            # Check whether this is enriched output
            if enriched:
                headers = ['target_domain', 'lookalike_domain', 
                           'registration_date', 'phishing', 'malware', 
                           'suspicious', 'categories', 'reason', 'registrar',
                           'last_updated', 'country', 'region',
                           'cert_issued_by', 'cert_expiry' ]
                w = csv.DictWriter(file, fieldnames=headers, extrasaction='ignore')
                w.writeheader()
                for l in lookalikes:
                    # Enrich lookalike 
                    r = self.enrich_lookalike(l)
                    w.writerow(l)

            else:
                # Simple Output
                headers = ['target_domain', 'lookalike_domain', 'registration_date', 
                        'phishing', 'malware', 'suspicious', 'categories', 'reason']

                try:
                    w = csv.DictWriter(file, fieldnames=headers, extrasaction='ignore')
                    w.writeheader()
                    w.writerows(lookalikes)
                except Exception as err:
                    logging.error(f'Error occured writing CSV: {err}')
                    raise
        else:
            logging.error('No data found')

        return
        

    def enrich_lookalike(self, record):
        '''
        '''
        sources = [ "geo", "whois", "ssl_cert" ]
        host = record.get('lookalike_domain')

        if host:
            response = self.dossierquery(host, type='host', sources=sources )
            if response.status_code in self.return_codes_ok:
                results = response.json().get('results')
                if results:
                    for r in results:
                        src = r.get('params').get('source')
                        data = r.get('data')
                        # Check data source
                        if src == 'whois':
                            if data.get('response'):
                                pw = data.get('response').get('parsed_whois')
                                if pw:
                                    registrar = pw.get('registrar').get('name')
                                    udate = pw.get('updated_date')
                                else:
                                    registrar = None
                                    udate = None
                            else:
                                registrar = None
                                udate = None
                        elif src == 'geo':
                            country = data.get('country_name')
                            region = data.get('region')
                        elif src == "ssl_cert":
                            ci = data.get('issuer')
                            ssl_chain = data.get('ssl_cert_chain')
                            if ssl_chain:
                                cert_exp = ssl_chain[0].get('expires')
                            else:
                                cert_exp = None

                    # Update record
                    enrichment = { 'registrar': registrar,
                                   'last_updated': udate,
                                   'country': country,
                                   'region': region,
                                   'cert_issued_by': ci,
                                   'cert_expiry': cert_exp }
                    
                    record.update(enrichment)
            else:
                logging.error(f'Could not enrich, API error: {response.status_code}')
        else:
            logging.error('No lookalike found in record')

        return record

"""
    def obfiscate_domains(self, data: list, fields: list):
        '''
        '''

        return
"""