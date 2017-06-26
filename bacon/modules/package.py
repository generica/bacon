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


Bacon module for package operations

Accepts a change structure for a change on a package
'''

import platform
import sys
import logging

LOGGER = logging.getLogger('bacon')

def detect_release():
    ''' Attempt to find out what OS sub-module we need '''

    if sys.platform == 'darwin':
        return 'darwin'
    elif sys.platform.startswith('linux'):
        # Figure out the distro
        distro = platform.linux_distribution()
        if distro[0] == 'debian':
            return 'debian'
        elif distro[0] == 'CentOS':
            return 'centos'
        else:
            try:
                with open("/etc/issue") as f:
                    return f.read().lower().split()[0]
            except:
                return 'unknown'
    elif sys.platform.startswith('freebsd'):
        return 'freebsd'
    else:
        LOGGER.error("Unsupported operating system")
        return None


def needs_change(change):
    ''' Detect if a change needs to occur or not '''

    change_type = "modules.%s.%s" % (detect_release(), change['type'])

    try:
        needs_change = getattr(__import__(change_type, fromlist=["needs_change"]), "needs_change")
    except ImportError:
        LOGGER.error("No support available for resource type: %s", change['type'])
        return

    return needs_change(change)


def perform_change(change):
    ''' Perform the change on the resource '''

    change_type = "modules.%s.%s" % (detect_release(), change['type'])

    try:
        perform_change = getattr(__import__(change_type, fromlist=["perform_change"]), "perform_change")
    except ImportError:
        LOGGER.error("No support available for resource type: %s", change['type'])
        return

    return perform_change(change)
