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

import argparse
import logging


def parse_arguments():
    ''' See what's up '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Increase verbosity',
                        action='store_true', required=False)
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
