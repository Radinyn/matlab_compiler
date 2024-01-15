from symbol_table import Symbol, SymbolTable
from abraham import Abraham

class NodeVisitor(object):


    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.content:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, Abraham.Node):
                            self.visit(item)
                elif isinstance(child, Abraham.Node):
                    self.visit(child)