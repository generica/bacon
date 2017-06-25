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


Bacon module for file operations

Accepts a change structure for a change on a file
'''

import os
import tempfile
import filecmp
import pwd
import grp


def populate_metadata(change):
    ''' Work out the metadata we'll end up with for a file '''

    if 'user' not in change:
        change['user'] = 'nobody'

    # FIXME: OS dependent. How do we define this?
    if 'group' not in change:
        change['group'] = 'nogroup'

    if 'mode' not in change:
        change['mode'] = 0644

    return change



def needs_change(change):
    ''' Detect if a change needs to occur or not '''

    # If the file doesn't exist, simple. Create it
    if not os.path.exists(change['path']):
        return True

    # Otherwise, let's make a temporary file and compare
    fp_change = populate_metadata(change)

    uid = pwd.getpwnam(fp_change['user']).pw_uid
    gid = grp.getgrnam(fp_change['group']).gr_gid

    fd, path = tempfile.mkstemp()

    os.write(fd, fp_change['content'])
    os.close(fd)
    os.chown(path, uid, gid)
    os.chmod(path, fp_change['mode'])

    different = filecmp.cmp(path, fp_change['path'])

    os.remove(path)

    return not different


def perform_change(change):
    ''' Perform the change on the resource '''

    fp_change = populate_metadata(change)

    uid = pwd.getpwnam(fp_change['user']).pw_uid
    gid = grp.getgrnam(fp_change['group']).gr_gid

    with open(fp_change['path'], 'w') as tmpf:
        tmpf.write(fp_change['content'])
        tmpf.close()

    os.chown(fp_change['path'], uid, gid)
    os.chmod(fp_change['path'], fp_change['mode'])
