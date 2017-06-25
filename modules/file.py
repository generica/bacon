#!/usr/bin/env python

'''
Bacon module for file operations

Accepts a change structure for a change on a file
'''

import os

def needs_change(change):
    ''' Detect if a change needs to occur or not '''

    # FIXME: Probably best to create the file we want, in a temp location, and
    #        use filecmp to see if it's how we want it.
    if not os.path.exists(change['path']):
        return True

    return False


def perform_change(change):
    ''' Perform the change on the resource '''

    with open(change['path'], 'w') as tmpf:
        tmpf.write(change['content'])
