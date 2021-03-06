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
import sys
import argparse
import logging
import pprint
from datetime import datetime
import yaml

LOGGER = logging.getLogger('bacon')


class Piggy(object):
    ''' A class to hold our final state, and any changes we want to apply '''

    def __init__(self, arguments):
        self.args = arguments
        self.changes = {}
        self.final_state = {}
        self.notify_list = []
        self.done_or_unneeded = []
        self.changes_skipped = []

    def parse_file(self, filename):
        ''' Parse a yaml file with instructions, and add it to our list '''

        with open(filename, 'r') as stream:
            try:
                self.final_state.update(yaml.load(stream))
            except yaml.YAMLError as exc:
                LOGGER.error(exc)

    def calculate_changes(self):
        ''' Work out what instructions we'll need to follow, and which ones will have no effect '''

        if not self.final_state:
            return

        for change_name, change in self.final_state.items():

            if 'type' not in change:
                LOGGER.error("No change type associated with named resource: %s", change_name)
                continue
            else:
                module_path = "bacon.modules.%s" % (change['type'])

            try:
                needs_change = getattr(__import__(module_path, fromlist=["needs_change"]), "needs_change")
            except ImportError:
                LOGGER.error("No support available for resource type: %s", change['type'])
                continue

            if needs_change(change):
                self.changes.update({change_name: change})
            else:
                self.done_or_unneeded.append(change_name)


    def apply_changes(self):
        ''' Apply the changes we've calculated '''

        self.changes_skipped = []

        for change_name, change in self.changes.items():

            if 'requires' in change:

                will_skip = False

                if not isinstance(change['requires'], list):
                    change['requires'] = [change['requires']]
                for req in change['requires']:
                    if req not in self.done_or_unneeded:
                        LOGGER.debug("Skipping %s for now, because of unmet requirement: %s", change_name, req)
                        self.changes_skipped.append(change_name)
                        will_skip = True
                if will_skip:
                    continue

            if 'type' not in change:
                LOGGER.error("No change type associated with named resource: %s", change_name)
                continue
            else:
                module_path = "bacon.modules.%s" % (change['type'])

            try:
                perform_change = getattr(__import__(module_path, fromlist=["perform_change"]), "perform_change")
            except ImportError:
                LOGGER.error("No support available for resource type: %s", change['type'])
                continue

            perform_change(change)

            self.done_or_unneeded.append(change_name)

            if 'notify' in change:
                if isinstance(change['notify'], list):
                    self.notify_list += change['notify']
                else:
                    self.notify_list += [change['notify']]


    def notify_changes(self):
        ''' Notify about the changes we've done '''

        for service in self.notify_list:
            LOGGER.debug("Will notify: %s", service)

            module_path = "bacon.modules.service"

            try:
                perform_reload = getattr(__import__(module_path, fromlist=["perform_change"]), "perform_change")
            except ImportError:
                LOGGER.error("No support available for resource type: service")
                continue

            # Grab our service, and set ensure to reload, then send it on
            if service in self.final_state:
                change = self.final_state[service]
                change['ensure'] = 'reload'

                perform_reload(change)
            else:
                LOGGER.error("Couldn't notify named service %s as it doesn't exist in manifest", service)


def parse_arguments():
    ''' See what's up '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Increase verbosity',
                        action='store_true', required=False)
    parser.add_argument('-t', '--test', help="Test only, don't apply changes",
                        action='store_true', required=False)
    parser.add_argument('-f', '--file', help='File to use for definitions',
                        action='append', required=False)

    return parser.parse_args()


def main():
    ''' Do some work '''

    start_time = datetime.now()

    args = parse_arguments()

    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)
    else:
        LOGGER.setLevel(logging.INFO)

    LOGGER.addHandler(logging.StreamHandler())

    if os.geteuid() != 0:
        LOGGER.warning("You are not running this as root. Expect failures")

    LOGGER.debug("Starting the sizzle")

    pig = Piggy(args)

    if pig.args.file:
        for pigfile in pig.args.file:
            pig.parse_file(pigfile)

    if not pig.final_state:
        LOGGER.debug("No changes defined")
        sys.exit(0)

    ppr = pprint.PrettyPrinter(indent=4)

    LOGGER.debug("We will end up with:")
    LOGGER.debug(ppr.pformat(pig.final_state))

    pig.calculate_changes()

    if not pig.changes:
        LOGGER.debug("No changes to be made")
    else:
        LOGGER.debug("Changes to apply:")
        LOGGER.debug(ppr.pformat(pig.changes))

        keep_trying = True

        if not args.test:
            while keep_trying:
                last_skipped = pig.changes_skipped
                pig.apply_changes()
                if last_skipped == pig.changes_skipped:
                    keep_trying = False

        if not args.test:
            pig.notify_changes()

    end_time = datetime.now()
    LOGGER.debug('Duration: %s', end_time - start_time)


if __name__ == "__main__":

    main()
