#!/usr/bin/env python3

from semantics_common import SymbolData, SemData

import lexer
import tree_builder
import tree_print
import semantic_checker
import semantic_run


if __name__ == '__main__':
    import argparse, codecs
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-t', '--treetype', help='Type of the tree (unicode/ascii/dot)')
    argument_group = argument_parser.add_mutually_exclusive_group()
    argument_group.add_argument('--who', action='store_true', help='author')
    argument_group.add_argument('-f', '--file', help='<FILE>')
    tree_formats = ('unicode', 'ascii', 'dot')
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
                syn_tree = tree_builder.parser.parse(data, lexer=lexer.lexer, debug=False)
                tree_print.treeprint(syn_tree)

                semdata = SemData()
                semdata.in_function = None
                check_result = semantic_checker.do_checks(syn_tree, semdata)
                if check_result is None:
                    print("semantics ok")
                semantic_run.run_program(syn_tree, semdata)

        except FileNotFoundError:
            print("File not found: '{}'".format(file))
            argument_parser.print_help()

