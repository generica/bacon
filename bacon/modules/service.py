#!/usr/bin/env python
# coding: utf-8

'''
BACON
Copyright (C) 2017 Brett Pemberton

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Bacon module for service operations

Accepts a change structure for a change on a service
'''

import logging

LOGGER = logging.getLogger('bacon')

def populate_metadata(change):
    ''' Work out the metadata we'll end up with for a service '''

    if 'manager' not in change:
        change['manager'] = 'sysv'

    return change


def needs_change(change):
    ''' Detect if a change needs to occur or not '''

    fp_change = populate_metadata(change)

    service = fp_change['name']
    ensure = fp_change['ensure']

    module_path = "bacon.modules.%s.%s" % (fp_change['manager'], 'service')

    try:
        our_service_is_running = getattr(__import__(module_path, fromlist=["service_is_running"]), "service_is_running")
    except ImportError:
        LOGGER.error("No support available for resource type: %s using manager %s", fp_change['type'], fp_change['manager'])
        return

    status = our_service_is_running(service)

    if ensure == "running":
        LOGGER.debug("Making sure %s is running. Status: %s", service, status)
        return not status
    elif ensure == "stopped":
        LOGGER.debug("Making sure %s is stopped. Status: %s", service, status)
        return status
    else:
        LOGGER.error("Unsupported service status: %s", ensure)

    return None


def perform_change(change):
    ''' Perform the change on the resource '''

    fp_change = populate_metadata(change)

    service = fp_change['name']
    ensure = fp_change['ensure']

    module_path = "bacon.modules.%s.%s" % (fp_change['manager'], 'service')

    try:
        our_perform_change = getattr(__import__(module_path, fromlist=["perform_change"]), "perform_change")
    except ImportError:
        LOGGER.error("No support available for resource type: %s using manager %s", fp_change['type'], fp_change['manager'])
        return

    return our_perform_change(service, ensure)
