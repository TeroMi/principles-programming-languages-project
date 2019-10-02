#!/usr/bin/env python3

import sys
import ply.lex as lex

tokens = (
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
    'EQUAL',
    'NOTEQUAL',
    'LESSTHAN',
    'LESSOREQUAL',
    'GREATTHAN',
    'GREATOREQUAL',
    'PLUS',
    'MINUS',
    'MULTIPLICATION',
    'DIVISION',
    'MODULUS',
    'NUMBER_LITERAL',
    'NEWLINE',
)

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
t_EQUAL = r'\='
t_NOTEQUAL = r'\!\='
t_LESSTHAN = r'\<'
t_LESSOREQUAL = r'\<\='
t_GREATTHAN = r'\>'
t_GREATOREQUAL = r'\>\='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'\/'
t_MODULUS = r'\%'

t_ignore = ' \t'


def t_COMMENT(t):
    r'\{((.|\s)*?)\}'


def t_NUMBER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


if __name__ == '__main__':
    import argparse, codecs
    argument_parser = argparse.ArgumentParser()
    argument_group = argument_parser.add_mutually_exclusive_group()
    argument_group.add_argument('--who', action='store_true', help='author')
    argument_group.add_argument('-f', '--file', help='input filename for lexical analysis')

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
            print("File not found: '{}'".format(file))

