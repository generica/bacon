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

import os
import logging
import commands
# FIXME: Replace with non-deprecated version

LOGGER = logging.getLogger('bacon')
BREW = '/usr/local/bin/brew'


def package_is_installed(package):
    ''' See if a package is installed or not '''

    # Check for brew
    if not (os.path.isfile(BREW) and os.access(BREW, os.X_OK)):
        LOGGER.error("brew not found in /usr/local/bin\nUnsupported operating system")
        raise OSError("Homebrew not installed")

    ourcommand = "%s ls --versions %s" % (BREW, package)

    status, _ = commands.getstatusoutput(ourcommand)

    # Package installed returns a 0 here for success, convert to True
    # Returns a 1 for failure, so convert to False

    return not bool(status)


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

    if ensure == "absent":
        command = "uninstall"
    elif ensure == "present":
        command = "install"
    else:
        LOGGER.error("Unsupported package status: %s", ensure)

    ourcommand = "%s %s %s" % (BREW, command, package)

    _, _ = commands.getstatusoutput(ourcommand)

    # FIXME: Check if it went ok?

    return True
