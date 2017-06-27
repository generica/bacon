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


LOGGER = logging.getLogger('bacon')

def package_is_installed(package):
    ''' See if a package is installed or not '''

    yumbase = yum.YumBase()

    return bool(yumbase.rpmdb.searchNevra(name=package))


def perform_change(change):
    ''' Perform the change on the resource '''

    package = change['name']
    ensure = change['ensure']

    yumbase = yum.YumBase()
    matches = yumbase.searchGenerator(['name'], [package])

    if ensure == "absent":
        LOGGER.debug("Uninstalling %s", package)
        for (package_obj, _) in matches:
            if package_obj.name == package:
                yumbase.remove(package_obj)
    elif ensure == "present":
        LOGGER.debug("Installing %s", package)
        for (package_obj, _) in matches:
            if package_obj.name == package:
                yumbase.install(package_obj)
    else:
        LOGGER.error("Unsupported package status: %s", ensure)
        return

    yumbase.buildTransaction()
    yumbase.processTransaction()

    # FIXME: Detect errors?

    return True
