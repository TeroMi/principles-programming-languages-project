from semantics_common import visit_tree, SymbolData, SemData


# check all variable, constant, tuple and function definitions and add them to symbol table
def populate_symbol_table(node, semdata):
    symtbl = semdata.symtbl

    if node.nodetype == 'var_definition':
        if node.value not in symtbl.keys():
            symtbl[node.value] = {"node_type": node.nodetype,
                                  "value": node.child_expression.value,
                                  "type": type(node.child_expression.value),
                                  "function_variable": False}
        else:
            symtbl[node.value]["value"] = node.child_expression.value
            symtbl[node.value]["type"] = type(node.child_expression.value)

    elif node.nodetype == 'const_definition':
        if node.value not in symtbl.keys():
            symtbl[node.value] = {"node_type": node.nodetype,
                                  "value": node.child_expression.value,
                                  "defined": True}
        elif symtbl[node.value]["defined"] is True:
            return "Constant variable '{}' is already defined".format(node.value)
        else:
            symtbl[node.value]["value"] = node.child_expression.value
            symtbl[node.value]["defined"] = True

    elif node.nodetype == 'tuple_definition':
        print("tuple def: '{}' '{}'".format(node.nodetype, node.value))
        if hasattr(node.child_expression, "children_argument"):
            for argument in node.child_expression.children_argument:
                asd = 1
                #print(argument.value)
        elif node.child_expression.nodetype == "function_call" and hasattr(node.child_expression, "children_arguments"):
            for argument in node.child_expression.children_arguments:
                asd = 1
                #print(argument.value)

    elif node.nodetype == 'function_definition':
        print("func def: '{}' '{}'".format(node.nodetype, node))

        if node.value not in symtbl.keys():
            symtbl[node.value] = {"node_type": node.nodetype,
                                  "value": node.child_return_value.child_expression.value,
                                  "defined": True}
        elif symtbl[node.value]["defined"] is True:
            return "Function '{}' is already defined".format(node.value)
        else:
            symtbl[node.value]["node_type"] = node.nodetype
            symtbl[node.value]["value"] = node.child_return_value.child_expression.value
            symtbl[node.value]["defined"] = True

        if len(node.children_formals) > 0:
            for formal in node.children_formals:
                #print(formal.value)
                if formal.value not in symtbl.keys():
                    symtbl[formal.value] = {"node_type": formal.nodetype,
                                            "value": "to_be_defined",
                                            "type": None,
                                            "function_variable": True}
        if len(node.children_variables) > 0:
            for variable in node.children_variables:
                print(variable.value)
                if hasattr(variable.child_expression, "value") and variable.value in symtbl.keys():
                    symtbl[variable.value]["value"] = variable.child_expression
                    symtbl[variable.value]["function_variable"] = True
                elif hasattr(variable.child_expression, "value"):
                    symtbl[variable.value] = {"node_type": variable.nodetype,
                                              "value": variable.child_expression.value,
                                              "type": type(variable.child_expression.value),
                                              "function_variable": True}

    elif node.nodetype == 'varIDENT':
        if node.value not in symtbl.keys():
            symtbl[node.value] = {"node_type": node.nodetype, "value": None, "function_variable": False}
        else:
            if symtbl[node.value]["function_variable"] is False:
                symtbl[node.value]["value"] = None

    elif node.nodetype == 'constIDENT':
        if node.value not in symtbl.keys():
            symtbl[node.value] = {"node_type": node.nodetype, "value": None, "defined": False}
        else:
            symtbl[node.value]["value"] = None

    elif node.nodetype == 'tupleIDENT':
        print("tuple ident: '{}' '{}'".format(node.nodetype, node.value))

    elif node.nodetype == 'function_call':
        print("function_call: '{}' '{}'".format(node.nodetype, node.value))
        if node.value not in symtbl.keys():
            symtbl[node.value] = {"node_type": node.nodetype, "value": None, "defined": False}
        else:
            symtbl[node.value]["defined"] = False


''' 
checks symbol table, if some variable/const/tuple has None value it is either not defined 
or has been used before the definition
'''
def check_symbol_table(node, semdata):
    print(semdata.symtbl)
    for name in semdata.symtbl:
        if semdata.symtbl[name]["value"] is None:
            if semdata.symtbl[name]["node_type"] in ('varIDENT', 'var_definition'):
                return "Variable '{}' not defined or used before definition!".format(name)
            elif semdata.symtbl[name]["node_type"] in ('constIDENT', 'const_definition'):
                return "Constant '{}' not defined or used before definition!".format(name)
            elif semdata.symtbl[name]["node_type"] in ('tupleIDENT', 'tuple_definiton'):
                return "Tuple '{}' not defined or used before definition!".format(name)
            elif semdata.symtbl[name]["node_type"] in ('function_call', 'function_definition'):
                return "Function '{}' not defined or used before definition!".format(name)


def do_checks(tree, semdata):
    visit_tree(tree, populate_symbol_table, None, semdata)
    # Visit tree is used to terminate checks if symbol table is not correct
    visit_tree(None, check_symbol_table, None, semdata)