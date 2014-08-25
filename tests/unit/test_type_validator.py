#!/usr/bin/env python
#
# type_base_test.py: unit tests for vyconf.types
#
# Copyright (C) 2014 VyOS Development Group <maintainers@vyos.net>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301
# USA

import unittest
import vyconf.types as types

class MockTypeSet(object):
    class FirstMockType(types.TypeValidator):
        name = "a_type"

    class SecondMockType(types.TypeValidator):
        name = "b_type"

class TestDummyValidators(unittest.TestCase):
    def test_get_types_keys(self):
        self.assertEqual(sorted(list(types.get_types(MockTypeSet).keys())), ["a_type", "b_type"])

    def test_get_types_values(self):
        self.assertTrue(issubclass(types.get_types(MockTypeSet)["a_type"], types.TypeValidator))

if __name__ == '__main__':
    unittest.main()

