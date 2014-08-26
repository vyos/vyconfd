#!/usr/bin/env python
#
# base_types_test.py: unit tests for vyconf.types.base
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
import vyconf.types.base as base

class TestBaseTypeValidators(unittest.TestCase):
    # StringValidator
    def test_string_valid(self):
        base.StringValidator.validate("fgsfds")

    def test_string_invalid_type(self):
        self.assertRaises(types.ValidationError, base.StringValidator.validate,
                          ({"foo": "bar"}))

    def test_string_invalid_constraint(self):
        self.assertRaises(types.ConstraintFormatError, base.StringValidator.validate,
                          "fgsfds", 42)

    def test_string_valid_constraint(self):
        base.StringValidator.validate("fgsfds", "[a-z]+")

    def test_string_doesnt_match_constraint(self):
        self.assertRaises(types.ValidationError, base.StringValidator.validate,
                          ("fgsfds", "[0-9]+"))

    # IntegerValidator
    def test_integer_valid(self):
        base.IntegerValidator.validate(42)

    def test_integer_invalid(self):
        # We don't want negative integers in configs
        self.assertRaises(types.ValidationError, base.IntegerValidator.validate, -42)

    def test_integer_from_string_valid(self):
        base.IntegerValidator.validate("9000")

    def test_integer_from_string_invalid(self):
        self.assertRaises(types.ValidationError, base.IntegerValidator.validate, "fgsfds")

    def test_integer_from_string_bad_constraint(self):
        self.assertRaises(types.ConstraintFormatError, base.IntegerValidator.validate,
                          "9000", "fgsfds")

    def test_integer_from_string_matches_constraint(self):
        base.IntegerValidator.validate("42", "0-42")

    def test_integer_from_string_multipart_constraint(self):
        base.IntegerValidator.validate("42", "10-15,40-92")

    def test_integer_from_string_doesnt_match_constraint(self):
        self.assertRaises(types.ValidationError, base.IntegerValidator.validate,
                          "9000", "10-15,9001-9003")

if __name__ == '__main__':
    unittest.main()

