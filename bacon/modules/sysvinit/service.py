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


Bacon module for sysvinit service operations

Accepts a change structure for a change on a package
'''

import logging
import os
import subprocess

LOGGER = logging.getLogger("bacon")

def service_is_running(service):
    ''' See if a service is running or not '''

    service_path = '/etc/init.d/%s' % (service)

    if not os.path.exists(service_path):
        LOGGER.error("Service %s not found", service)
        return False

    result = subprocess.call([service_path, "status"], stdout=subprocess.DEVNULL)

    return not bool(result)


def perform_change(service, ensure):
    ''' Perform the change on the resource '''

    service_path = os.path.join(os.path.sep, 'etc', 'init.d', service)

    if not os.path.exists(service_path):
        LOGGER.error("Service %s not found", service)
        return False

    if ensure == 'running':
        subprocess.call([service_path, 'start'])
    elif ensure == 'stopped':
        subprocess.call([service_path, 'stop'])
    elif ensure == 'reload':
        subprocess.call([service_path, 'reload'])

    return None
