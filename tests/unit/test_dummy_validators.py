#!/usr/bin/env python
#
# dummy_validators_test.py: unit tests for vyconf.types.dummy dummy validators
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
import vyconf.types
import vyconf.types.dummy as dummy


class TestDummyValidators(unittest.TestCase):
    def test_always_valid(self):
        dummy.AlwaysValid.validate("fgsfds")

    def test_never_valid(self):
        self.assertRaises(vyconf.types.ValidationError,
                          dummy.NeverValid.validate,
                          "fgsfds")

    def test_bad_constraint(self):
        self.assertRaises(vyconf.types.ConstraintFormatError,
                          dummy.BadConstraint.validate,
                          ["fgsfds", "dsgfd"])


if __name__ == '__main__':
    unittest.main()

