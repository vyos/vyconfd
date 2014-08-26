#!/usr/bin/env python
#
#    curly_parser_test.py:  tests for vyconf.configfile.curly.Parser
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


import vyconf.configfile.curly
import unittest

# Comparing to a complete datastructure is sort of ugly, but I don't see
# a better way to make sure it works correctly yet.

class TestCurlyParser(unittest.TestCase):
    def setUp(self):
        self.parser = vyconf.configfile.curly.Parser()

    def test_empty_config(self):
        self.assertRaises(vyconf.configfile.curly.ParseError, self.parser.parse, "")

    def test_single_empty_node(self):
        parser = vyconf.configfile.curly.Parser()
        result = [('node', {'comment': None, 'content': None, 'name': ['foo']})]
        ast = parser.parse("foo { }",positiontracking=False)
        self.assertEqual(ast, result)

    def test_single_node_with_comment(self):
        result = [('node', {'comment': 'Foo', 'content': None, 'name': ['foo']})]
        ast = self.parser.parse("/* Foo */ foo {}",positiontracking=True)
        self.assertEqual(ast, result)

    def test_single_non_empty_node(self):
        result = [('node', {'comment': None, 'content':
                   [('leaf-node', {'comment': None, 'name': ['bar'], 'value': 0})], 'name': ['foo']})]
        ast = self.parser.parse("foo { bar 0; }")
        self.assertEqual(ast, result)

    def test_leaf_single_leaf_node_with_comment(self):
        result = [('node', {'comment': None, 'content':
                   [('leaf-node', {'comment': 'Foo', 'name': ['bar'], 'value': 0})], 'name': ['foo']})]
        ast = self.parser.parse("foo { /* Foo */ bar 0; }")
        self.assertEqual(ast, result)

    def test_multiple_leaf_nodes(self):
        result = [('node', {'comment': None, 'content':
                              [('leaf-node', {'comment': 'Foo', 'name': ['bar'], 'value': 0}),
                               ('leaf-node', {'comment': None, 'name': ['baz'], 'value': 'quux'})],
                            'name': ['foo']})]
        ast = self.parser.parse(""" foo {  /* Foo */ bar 0; baz "quux"; } """)
        self.assertEqual(ast, result)



if __name__ == '__main__':
    unittest.main()
