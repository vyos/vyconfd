#    vyconf.configfile.curly.parser: parser for the curly config
#
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

# -- I'd prefer not to argue about politics.
# -- It's not a question of politics, but of grammar.
# -- In that case, I'd rather not argue about grammar.
#                  Lipson, Molinsky, "A Russian Course"

import ply.yacc as yacc
from .lexer import Lexer

class ParseError(Exception):
    """ Raised when incorrect token is found
    """
    def __init__(self, token):
        token_str = ""
        position = ""
        if token:
            token_str = token.value
            position = token.lineno
        message = "Unexpected token '{0}' at line {1}".format(token_str, position)
        super(ParseError, self).__init__(message)
        self.strerror = message


class Parser(object):
    def __init__(
            self,
            lex_optimize=True,
            yacc_optimize=True,
            yacc_debug=False):
        self.lexer = Lexer()

        self.lexer.build(
            optimize=lex_optimize,
            )
        self.tokens = self.lexer.tokens

        self.parser = yacc.yacc(
            module=self,
            start='config',
            debug=yacc_debug,
            optimize=yacc_optimize)

    def parse(self, text, filename='', debuglevel=0,positiontracking=True):
        self.lexer.filename = filename
        self._last_yielded_token = None
        return self.parser.parse(
                input=text,
                lexer=self.lexer,
                debug=debuglevel,
                tracking=positiontracking)

    def p_value(self, p):
        ''' value : IDENTIFIER
                  | STRING
        '''
        p[0] = p[1]

    def p_leaf_node(self, p):
        ''' leaf_node : node_comment IDENTIFIER value SEMICOLON
                      | IDENTIFIER value SEMICOLON
                      | IDENTIFIER SEMICOLON
                      | node_comment IDENTIFIER SEMICOLON
        '''
        p_tmp = None
        if len(p) == 3:
            # Typeless node without comment
            p_tmp = {"name": [p[1]], "value": None, "comment": None}
        elif len(p) == 4:
            # Typeless node with comment,
            # or node with value
            if p[0] == "comment":
                # Typeless with comment
                p_tmp = {"name": [p[2]], "value": None, "comment": p[1][1]}
            else:
                # Node with value
                p_tmp = {"name": [p[1]], "value": p[2], "comment": None}
        elif len(p) == 5:
            # Node with value and comment
            p_tmp = {"name": [p[2]], "value": p[3], "comment": p[1][1]}

        p[0] = ('leaf-node', p_tmp)

    def p_leaf_nodes(self, p):
        ''' leaf_nodes : leaf_node
                       | leaf_nodes leaf_node
        '''
        if len(p) == 2:
            # The first node in group, make a list of it
            p[0] = [p[1]]
        else:
            # There already are nodes, append it to the list
            p[0] = p[1] + [p[2]]

    def p_node_comment(self, p):
        ''' node_comment : NODE_COMMENT '''
        p[0] = ('comment', p[1])

    def p_node_name(self, p):
        ''' node_name : IDENTIFIER
                      | IDENTIFIER IDENTIFIER
        '''
        if len(p) < 3:
            # That's ordinary node with one-word name
            node_name = [p[1]]
        else:
            # That's a tag node
            node_name = [p[1], p[2]]

        p[0] = ('node-name', node_name)

    def p_node_content(self, p):
        ''' node_content : leaf_nodes
                         | leaf_nodes nodes
                         | nodes leaf_nodes
                         | leaf_nodes nodes leaf_nodes
                         | nodes
        '''
	# This is to avoid producing a nested list
        # when there are leaf/non-leaf nodes mixed together,
        # since we return those as lists
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2]

    def p_nodes(self, p):
        ''' nodes : node
                  | nodes node
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_node(self, p):
        ''' node : node_name LBRACE node_content RBRACE
                 | node_comment node_name LBRACE node_content RBRACE
                 | node_name LBRACE RBRACE
                 | node_comment node_name LBRACE RBRACE
        '''
        if len(p) == 4:
            # Empty node without comment
            p[0] = ('node', {"comment": None, "name": p[1][1], "content": None})
        elif len(p) == 5:
            if p[2] == '{':
                # Non-empty node without comment
                p[0] = ('node', {"comment": None, "name": p[1][1], "content": p[3]})
            else:
                # Empty node with comment
                p[0] = ('node', {"comment": p[1][1], "name": p[2][1], "content": None})
        else:
            # Non-empty node with comment
            p[0] = ('node', {"comment": p[1][1], "name": p[2][1], "content": p[4]})

    def p_config(self, p):
        ''' config : nodes '''

        p[0] = p[1]

    def p_error(self, p):
        raise ParseError(p)
