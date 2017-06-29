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

def detect_linux_release():
    ''' Attempt to find out what Linux sub-module we need '''

    distro = platform.linux_distribution()
    if distro[0] == 'debian' or distro[0].lower() == 'ubuntu':
        return 'debian'
    elif distro[0] == 'CentOS':
        return 'centos'
    else:
        try:
            with open("/etc/issue") as issue:
                issue = issue.read().lower().split()[0]
                if issue.lower() == 'amazon':
                    return 'centos'
                else:
                    return issue
        except IOError:
            return 'unknown'


def detect_release():
    ''' Attempt to find out what OS sub-module we need '''

    if sys.platform == 'darwin':
        return 'darwin'
    elif sys.platform.startswith('linux'):
        return detect_linux_release()
    elif sys.platform.startswith('freebsd'):
        return 'freebsd'
    else:
        LOGGER.error("Unsupported operating system")
        return None


def needs_change(change):
    ''' Detect if a change needs to occur or not '''

    package = change['name']
    ensure = change['ensure']

    release = detect_release()

    module_path = "bacon.modules.%s.%s" % (detect_release(), 'package')

    try:
        distro_package_is_installed = getattr(__import__(module_path, fromlist=["package_is_installed"]), "package_is_installed")
    except ImportError:
        LOGGER.error("No support available for resource type: %s on OS %s", change['type'], release)
        return

    status = distro_package_is_installed(package)

    if ensure == "absent":
        LOGGER.debug("Making sure %s is not here. Status: %s", package, status)
        return status
    elif ensure == "present":
        LOGGER.debug("Making sure %s is here. Status: %s", package, status)
        return not status
    else:
        LOGGER.error("Unsupported package status: %s", ensure)

    return None


def perform_change(change):
    ''' Perform the change on the resource '''

    release = detect_release()
    module_path = "bacon.modules.%s.%s" % (release, change['type'])

    try:
        distro_perform_change = getattr(__import__(module_path, fromlist=["perform_change"]), "perform_change")
    except ImportError:
        LOGGER.error("No support available for resource type: %s on OS %s", change['type'], release)
        return

    return distro_perform_change(change)
