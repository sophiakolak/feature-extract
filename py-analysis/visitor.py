import ast 

class Visitor(ast.NodeVisitor):
    def generic_visit(self, node):
        #print(f'Nodetype: {type(node).__name__:{16}} {node}')
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)


