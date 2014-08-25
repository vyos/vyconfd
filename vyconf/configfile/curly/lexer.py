#    vyconf.configfile.curly.lexer: lexer for the curly config
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

import ply.lex as lex
import re

class Lexer(object):

    __number_regex = re.compile('\d+')

    # Multiline comment can't be extracted with regex,
    # so we have exclusive state for it
    states = (
         ('COMMENT', 'exclusive'),
    )

    tokens = (
        'LBRACE',
        'RBRACE',
        'IDENTIFIER',
        'STRING',
        'NODE_COMMENT',
        'SEMICOLON',
    )

    t_LBRACE = r'\{'
    t_RBRACE  = r'\}'
    t_SEMICOLON = r';'

    # /* */ comment. This is a bit complicated.
    # VyConf is supposed to store node comments along with nodes
    # and display them in the config etc., that's why all the hassle

    def t_COMMENT(self, t):
        r'/\*'
        t.lexer.code_start = t.lexer.lexpos
        t.lexer.level = 1
        t.lexer.begin('COMMENT')

    t_COMMENT_ignore = '\n'

    def t_COMMENT_anything(self, t):
        r'(\s|\w)+'

    def t_COMMENT_error(self, t):
        print("Illegal character '{0}'".format(t.value[0]))
        t.lexer.skip(1)

    def t_COMMENT_end(self, t):
        r'\*/'
        tmp_str = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos-2]
        t.value = tmp_str.strip()
        t.type = "NODE_COMMENT"
        t.lexer.lineno += t.value.count('\n')
        t.lexer.begin('INITIAL')
        return t
    # The comment stuff is over

    # Define a rule so we can track line numbers
    def t_NEWLINE(self, t):
        r'\n+'

        t.lexer.lineno += len(t.value)
        return t

    def t_IDENTIFIER(self, t):
        r'[^\s;{}\"\']+'

        if re.match(self.__number_regex, t.value):
            t.value = int(t.value)

        return t

    def t_STRING(self, t):
        r'\"([^\\"]|(\\.))*\"'

        escaped = 0
        str = t.value[1:-1]
        new_str = ""
        for i in range(0, len(str)):
            c = str[i]
            if escaped:
                if c == "n":
                    c = "\n"
                elif c == "t":
                    c = "\t"
                new_str += c
                escaped = 0
            else:
                if c == "\\":
                    escaped = 1
                else:
                    new_str += c
        t.value = new_str
        return t

    t_ignore  = ' \t\n'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '{0}'".format(t.value[0]))
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token
