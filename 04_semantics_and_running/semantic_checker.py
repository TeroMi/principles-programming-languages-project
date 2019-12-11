from semantics_common import visit_tree, SymbolData, SemData


# Checks if variable has been defined before use
def check_definition_before_use(node, semdata):
    symtbl = semdata.symtbl
    if node.nodetype == 'variable definition':
        print("var def: '{}' '{}'".format(node.nodetype, node.value))
        symtbl[str(node.value)] = node.child_expression.value
    elif node.nodetype == 'const_definition':
        print("const def: '{}' '{}'".format(node.nodetype, node))
    elif node.nodetype == 'tuple_definition':
        print("tuple def: '{}' '{}'".format(node.nodetype, node))
    elif node.nodetype == 'function_definition':
        print("func def: '{}' '{}'".format(node.nodetype, node))

    elif node.nodetype == 'varIDENT':
        print("var ident: '{}' '{}'".format(node.nodetype, node.value))
        try:
            if symtbl[node.value]:
                return "Variable '{}' not defined!".format(node.value)
        except:
            print("Variable defined")
    elif node.nodetype == 'constIDENT':
        print("const ident: '{}' '{}'".format(node.nodetype, node.value))
    elif node.nodetype == 'tuple identifier':
        print("tuple ident: '{}' '{}'".format(node.nodetype, node.value))
    elif node.nodetype == 'function_call':
        print("function_call: '{}' '{}'".format(node.nodetype, node.value))


def do_checks(tree, semdata):
    visit_tree(tree, check_definition_before_use, None, semdata)
    print(semdata.symtbl)