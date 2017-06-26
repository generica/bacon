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

import logging
import yum


LOGGER = logging.getLogger(__name__)

def package_is_installed(package):
    ''' See if a package is installed or not '''

    yb = yum.YumBase()

    if yb.rpmdb.searchNevra(name=package):
        return True
    else:
        return False


def needs_change(change):
    ''' Detect if a change needs to occur or not '''

    package = change['name']
    ensure = change['ensure']

    status = package_is_installed(package)

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

    package = change['name']
    ensure = change['ensure']

    yb = yum.YumBase()
    matches = yb.searchGenerator(['name'], [package])

    if ensure == "absent":
        LOGGER.debug("Uninstalling %s", package)
        for (package_obj, matched_value) in matches:
            if package_obj.name == package:
                yb.remove(package_obj)
    elif ensure == "present":
        LOGGER.debug("Installing %s", package)
        for (package_obj, matched_value) in matches:
            if package_obj.name == package:
                yb.install(package_obj)
    else:
        LOGGER.error("Unsupported package status: %s", ensure)
        return

    yb.buildTransaction()
    yb.processTransaction()

    # FIXME: Detect errors?

    return True
