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

'''

from __future__ import print_function
import os
import argparse
import logging
import yaml


class Piggy(object):
    ''' A class to hold our final state, and any changes we want to apply '''

    def __init__(self, arguments):
        self.args = arguments
        self.changes = {}
        self.final_state = None

    def parse_file(self, filename):
        ''' Parse a yaml file with instructions, and add it to our list '''

        with open(filename, 'r') as stream:
            try:
                self.final_state = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def calculate_changes(self):
        ''' Work out what instructions we'll need to follow, and which ones will have no effect '''

        for changeName, change in self.final_state.items():
            LOGGER.debug(change)
            if change['type'] == 'file':
                # FIXME: Probably best to create the file we want, in a temp location, and
                #        use filecmp to see if it's how we want it.
                if not os.path.exists(change['path']):
                    ''' Doesn't exist at all, definitely add this to changes needed '''
                    self.changes.update({changeName: change})

    def apply_changes(self):
        ''' Apply the changes we've calculated '''

        for changeName, change in self.changes.items():
            if change['type'] == 'file':
                with open(change['path'],'w') as f:
                    f.write(change['content'])

def parse_arguments():
    ''' See what's up '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Increase verbosity',
                        action='store_true', required=False)
    parser.add_argument('-t', '--test', help="Test only, don't apply changes",
                        action='store_true', required=False)
    parser.add_argument('-f', '--file', help='File to use for definitions',
                        action='store', required=False)

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_arguments()

    # Root logger configuration
    LOGGER = logging.getLogger(__name__)
    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)
    else:
        LOGGER.setLevel(logging.INFO)

    LOGGER.addHandler(logging.StreamHandler())

    LOGGER.debug("Starting the sizzle")

    pig = Piggy(args)

    # TODO: Allow multiple files? How to deal with duplicate conflicting definitions
    #       Actually, we'll have to solve that regardless
    if pig.args.file:
        pig.parse_file(pig.args.file)

    LOGGER.debug("We will end up with:")
    LOGGER.debug(pig.final_state)

    pig.calculate_changes()

    LOGGER.debug("Changes to apply:")
    LOGGER.debug(pig.changes)

    pig.apply_changes()
