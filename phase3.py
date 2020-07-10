#!/usr/local/bin/python3
#vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
'''
------------------------------------------------------------------------

 Description:

 Requirements:
   Python3 with re, ipaddress, requests and sqlite3 modules

 Author: Chris Marrison

 Date Last Updated: 20200605

 Todo:

 Copyright (c) 2018 Chris Marrison / Infoblox

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
__version__ = '0.0.2'
__author__ = 'Chris Marrison'
__author_email__ = 'chris@infoblox.com'

import bloxone
import os
import json
import argparse
import logging
import datetime


# Global Variables
log = logging.getLogger(__name__)

def parseargs():
    '''
    Parse Arguments Using argparse

    Parameters:
        None

    Returns:
        Returns parsed arguments
    '''
    parse = argparse.ArgumentParser(description='B1DDI Phase 3 Training Assignment')
    # parse.add_argument('-o', '--output', type=str,
                       # help="Output to <filename>")
    parse.add_argument('-c', '--config', type=str, default='config.ini',
                       help="Overide Config file")
    parse.add_argument('-d', '--debug', action='store_true', help="Enable debug messages")
    parse.add_argument('username', type=str, help="Username for Owner Tag")

    return parse.parse_args()


def setup_logging(debug):
    '''
     Set up logging

     Parameters:
        debug (bool): True or False.

     Returns:
        None.

    '''
    # Set debug level
    if debug:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO,
                            format='%(levelname)s: %(message)s')
                            # format='%(asctime)s %(levelname)s: %(message)s')

    return


def open_file(filename):
    '''
    Attempt to open output file

    Parameters:
        filename (str): desired filename

    Returns file handler
        handler (file): File handler object
    '''
    if os.path.isfile(filename):
        backup = filename+".bak"
        try:
            shutil.move(filename, backup)
            log.info("Outfile exists moved to {}".format(backup))
            try:
                handler = open(filename, mode='w')
                log.info("Successfully opened output file {}.".format(filename))
            except IOError as err:
                log.error("{}".format(err))
                handler = False
        except:
            log.warning("Could not back up existing file {}, exiting.".format(filename))
            handler = False
    else:
        try:
            handler = open(filename, mode='w')
            log.info("Opened file {} for invalid lines.".format(filename))
        except IOError as err:
            log.error("{}".format(err))
            handler = False

    return handler


def check_on_prem(b1ddi, username):
    '''
    Validate on prem hosts
    '''
    status = False
    grid = False
    results = {}
    tfilter = 'Owner==' + username
    count = 0
    gcount = 0
    report = {}
    correct_tag_count = 0

    # response, results = b1ddi.on_prem_hosts()
    response, results = b1ddi.on_prem_hosts(_tfilter=tfilter)
    results = json.loads(results)

    if len(results):
        for host in results['result']:
            if host['host_type'] == "6":
                # Grid Connector
                gcount += 1
                grid = True
                log.info("*** Grid Connector Found.")
            else:
                count += 1
                log.info("*** BloxOne DDI Host Found.")

            log.info('Display Name: {}'.format(host['display_name']))
            log.info('Last Seen: {}'.format(host['last_seen']))
            log.info('Tags:')
            # Output tags
            for tag in host['tags']:
                log.info("{}: {}".format(tag, host['tags'][tag]))
            # Check for Owner and Location
            if "Owner" in host['tags'].keys() and "Location" in host['tags'].keys():
                correct_tag_count += 1 
                log.info("*** Owner & Location tags set.")
            else:
                log.info("*** Location tag not set on: {}".format(host['display_name']))
        log.info("*** Number of on prem hosts found: {}".format(count))
        log.info("*** Number of on Grid Connectors found: {}".format(gcount))
        # Check number of BloxOneDDI On Prem Hosts
        if count >= 2:
            status = True
        else:
            status = False
        
        # All tagged?
        if correct_tag_count == (count + gcount):
            log.info("*** All tagged with Owner and Location.")
        else:
            log.info("*** Not all correctly tagged.")

    else:
        log.info("*** No on prem hosts found.")
        log.info()
        status = False

    report = { "B1DDI Hosts": status, "Grid": grid }

    return report


# *** Main ***
args = parseargs()
username = args.username
# outputfile = args.output
inifile = args.config
debug = args.debug

setup_logging(debug)

b1ddi = bloxone.b1ddi(inifile)
status = check_on_prem(b1ddi, username)
log.info(status)

# b1ddi.dhcp_range(_tfilter='"Owner"="jcanelada"')