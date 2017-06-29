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

import unittest
import os
from bacon.bacon import Piggy

class BaconTest(unittest.TestCase):
    localstore = os.getcwd()
    tests_directory = "/bacon/test/"

    def setUp(self):
        if "/test" in self.__class__.localstore:
            self.__class__.tests_directory = "/"
        pass

    def test_blank(self):
        ''' Test blank '''

        pig = Piggy(None)
        self.assertEqual(pig.final_state, {})
        self.assertEqual(pig.changes, {})

if __name__ == '__main__':
    unittest.main()
