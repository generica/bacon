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
import commands
# FIXME: Replace with a non-deprecated method
import logging

LOGGER = logging.getLogger(__name__)
APT_GET="/usr/bin/apt-get"

def needs_change(change):
    ''' Detect if a change needs to occur or not '''

    return True


def perform_change(change):
    ''' Perform the change on the resource '''

    # Check for apt-get
    if not (os.path.isfile(APT_GET) and os.access(APT_GET, os.X_OK)):
        LOGGER.error("apt-get not found in /usr/bin\nUnsupported operating system")
        return False
