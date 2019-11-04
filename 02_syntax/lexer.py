#!/usr/bin/env python3

import sys
import re
import ply.lex as lex

reserved = {
    'define': 'DEFINE',
    'begin': 'BEGIN',
    'end': 'END',
    'each': 'EACH',
    'select': 'SELECT',
}

tokens = [
    'COMMENT',
    'LARROW',
    'RARROW',
    'LPAREN',
    'RPAREN',
    'LSQUARE',
    'RSQUARE',
    'COMMA',
    'DOT',
    'PIPE',
    'DOUBLEPLUS',
    'DOUBLEMULT',
    'DOUBLEDOT',
    'COLON',
    'EQ',
    'NOTEQ',
    'LT',
    'LTEQ',
    'GT',
    'GTEQ',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'MOD',
    'NUMBER_LITERAL',
    'STRING_LITERAL',
    'varIDENT',
    'constIDENT',
    'tupleIDENT',
    'funcIDENT',
    'NEWLINE',
    'ID'
] + list(reserved.values())

t_LARROW = r'<-'
t_RARROW = r'->'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_COMMA = r'\,'
t_DOT = r'\.'
t_PIPE = r'\|'
t_DOUBLEPLUS = r'\+\+'
t_DOUBLEMULT = r'\*\*'
t_DOUBLEDOT = r'\.\.'
t_COLON = r'\:'
t_EQ = r'\='
t_NOTEQ = r'\!\='
t_LT = r'\<'
t_LTEQ = r'\<\='
t_GT = r'\>'
t_GTEQ = r'\>\='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'
t_MOD = r'\%'

t_ignore = ' \t\r\n'


def t_COMMENT(t):
    r'\{((.|\s)*?)\}'
    comment_line_count = t.value.count('\n')
    t.lexer.lineno += comment_line_count


def t_NUMBER_LITERAL(t):
    r'(0|\d+)'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'"(.|\s)*?"'
    t.value = t.value.replace("\"", "")
    return t


def t_varIDENT(t):
    r'\b[a-z][a-zA-Z0-9_]+'
    return t


def t_constIDENT(t):
    r'\b[A-Z]+\b'
    return t


def t_tupleIDENT(t):
    r'<[a-z]+>'
    return t


def t_funcIDENT(t):
    r'\b[A-Z][a-z0-9_]+\b'
    return t


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    error_line = re.split('\n', t.value)[0]
    if error_line == "":
        error_line = ""
    else:
        error_line = ", in input: \n{}\n^".format(error_line)
    print("Illegal character '{}' at line {}{}".format(t.value[0], t.lexer.lineno, error_line))

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

lexer = lex.lex()


if __name__ == '__main__':
    import argparse, codecs
    argument_parser = argparse.ArgumentParser()
    argument_group = argument_parser.add_mutually_exclusive_group()
    argument_group.add_argument('--who', action='store_true', help='author')
    argument_group.add_argument('-f', '--file', help='<FILENAME>.tupl')

    input_args_parsed = argument_parser.parse_args()
    if input_args_parsed.who:
        print("Author: 283121 Tero Mielikäinen")
    elif input_args_parsed.file is None:
        argument_parser.print_help()
    else:
        file = input_args_parsed.file
        try:
            with codecs.open(file, 'r') as INFILE:
                data = INFILE.read()
                lexer.input(data)

                for token in lexer:
                    print(token)
        except FileNotFoundError:
            print("File not found: '{}', maybe you forgot or mistyped the suffix".format(file))
        except lex.LexError as lexError:
            if "Illegal" not in str(lexError):
                print("Shutting down lexer because of error: \n {}".format(lexError))
            else:
                print("Shutting down ..")

"""
NOTES:
STRING_LITERAL does not remove "-characters from the string literal
Reserved words could be done also without having separate rules for all of them.
Remember to ignore line feeds too \r
"""