#!/usr/bin/env python
#
#    config_node_test.py: unit tests for vyconf.tree.Node
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


import vyconf.tree.configtree
import unittest


class TestVytreeConfigNode(unittest.TestCase):
    def test_add_value(self):
        node = vyconf.tree.configtree.ConfigNode('root')
        node.add_value("foo")
        self.assertEqual(node.get_values(), ["foo"])

    def test_remove_value(self):
        node = vyconf.tree.configtree.ConfigNode('root')
        node.add_value("foo")
        node.add_value("bar")
        node.remove_value("foo")
        self.assertEqual(node.get_values(), ["bar"])

    def test_get_comment_before_its_set(self):
        node = vyconf.tree.configtree.ConfigNode('root')
        self.assertIsNone(node.get_comment())

    def test_set_comment(self):
        node = vyconf.tree.configtree.ConfigNode('root')
        node.set_comment("This is a comment")
        self.assertEqual(node.get_comment(), "This is a comment")


if __name__ == '__main__':
    unittest.main()

