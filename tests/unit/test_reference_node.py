#!/usr/bin/env python
#
#    reference_node_test.py: unit tests for vyconf.tree.referencetree.ReferenceNode
#    Copyright (C) 2014 VyOS Development Group <maintainers@vyos.net>
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#    USA


import vyconf.tree.referencetree
import unittest


class TestVytreeReferenceNode(unittest.TestCase):
    def test_leaf(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        node.set_leaf()
        self.assertTrue(node.is_leaf())

    def test_leaf_default(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        self.assertFalse(node.is_leaf())

    def test_tag(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        node.set_tag()
        self.assertTrue(node.is_tag())

    def test_tag_default(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        self.assertFalse(node.is_tag())

    def test_multi(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        node.set_multi()
        self.assertTrue(node.is_multi())

    def test_multi_default(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        self.assertFalse(node.is_multi())

    def test_name_constraint(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        node.set_name_constraint("foo", "bar")
        self.assertEqual(node.get_name_constraint(), {"type": "foo",
                                                      "constraint": "bar",
                                                      "error_message": None})

    def test_name_constraint_with_message(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        node.set_name_constraint("foo", "bar", "baz")
        self.assertEqual(node.get_name_constraint(), {"type": "foo",
                                                      "constraint": "bar",
                                                      "error_message": "baz"})

    def test_name_constraint_default(self):
       	node = vyconf.tree.referencetree.ReferenceNode('root')
        self.assertFalse(node.get_name_constraint())

    def test_value_constraints(self):
       	node = vyconf.tree.referencetree.ReferenceNode('root')
        node.add_value_constraint("foo", "bar")
        self.assertEqual(node.get_value_constraints(), [{"type":
                                                         "foo",
                                                         "constraint": "bar",
                                                         "error_message": None}])

    def test_value_constraints_with_message(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        node.add_value_constraint("foo", "bar", "baz")
        self.assertEqual(node.get_value_constraints(), [{"type":
                                                         "foo",
                                                         "constraint": "bar",
                                                         "error_message": "baz"}])

    def test_value_constraints_multiple(self):
       	node = vyconf.tree.referencetree.ReferenceNode('root')
        node.add_value_constraint("foo", "bar")
        node.add_value_constraint("baz", "quux")
        self.assertEqual(node.get_value_constraints(), [{"type": "foo",
                                                         "constraint": "bar",
                                                         "error_message": None},
                                                        {"type": "baz",
                                                         "constraint": "quux",
                                                         "error_message": None}])

    def test_value_constraints_default(self):
       	node = vyconf.tree.referencetree.ReferenceNode('root')
        self.assertEqual(node.get_value_constraints(), [])

    def test_value_help_strings(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        node.add_value_help_string("foo", "Foo value")
        self.assertEqual(node.get_value_help_strings(), [{"format": "foo", "help": "Foo value"}])

    def test_value_help_strings_multiple(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        node.add_value_help_string("foo", "bar")
        node.add_value_help_string("baz", "quux")
        self.assertEqual(node.get_value_help_strings(), [{"format": "foo", "help": "bar"},
                                                         {"format": "baz", "help": "quux"}])

    def test_value_help_strings_default(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        self.assertEqual(node.get_value_help_strings(), [])

    def test_help_string(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        node.set_help_string("foo")
        self.assertEqual(node.get_help_string(), "foo")

    def test_help_string_default(self):
        node = vyconf.tree.referencetree.ReferenceNode('root')
        self.assertEqual(node.get_help_string(), "")


if __name__ == '__main__':
    unittest.main()

