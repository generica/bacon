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
import logging

LOGGER = logging.getLogger('bacon')


def populate_metadata(change):
    ''' Work out the metadata we'll end up with for a file '''

    if 'user' not in change:
        change['user'] = 'nobody'

    # FIXME: OS dependent. How do we define this?
    if 'group' not in change:
        change['group'] = 'nogroup'

    if 'mode' not in change:
        change['mode'] = '0644'

    if 'ensure' not in change:
        change['ensure'] = 'absent'

    return change

def needs_change(change):
    ''' Detect if a change needs to occur or not '''

    fp_change = populate_metadata(change)

    if fp_change['ensure'] == 'absent':
        # Simple scenario. If the file exists, nuke it
        # Wait, not so simple. If this has a dependency on a package,
        # And the file is installed by the package, then we have a race.
        # Let's just always make sure the file is gone
        return True

    # Now that we're here, ensure must be present

    # If the file doesn't exist, simple. Create it
    if not os.path.exists(fp_change['path']):
        return True

    # Otherwise, let's make a temporary file and compare

    uid = pwd.getpwnam(fp_change['user']).pw_uid
    gid = grp.getgrnam(fp_change['group']).gr_gid

    fdesc, path = tempfile.mkstemp()

    os.write(fdesc, fp_change['content'].encode())
    os.close(fdesc)
    os.chown(path, uid, gid)
    os.chmod(path, int(fp_change['mode']))

    different = filecmp.cmp(path, fp_change['path'])

    os.remove(path)

    return not different


def perform_change(change):
    ''' Perform the change on the resource '''

    fp_change = populate_metadata(change)

    if fp_change['ensure'] == 'absent':
        try:
            os.remove(fp_change['path'])
        except FileNotFoundError:
            LOGGER.debug("Tried to remove a nonexistent file")
        return True

    uid = pwd.getpwnam(fp_change['user']).pw_uid
    gid = grp.getgrnam(fp_change['group']).gr_gid

    with open(fp_change['path'], 'w') as tmpf:
        tmpf.write(fp_change['content'])
        tmpf.close()

    os.chown(fp_change['path'], uid, gid)
    os.chmod(fp_change['path'], int(fp_change['mode']))
