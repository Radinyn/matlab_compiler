#!/usr/bin/python

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node)

class Tytus(NodeVisitor):

    def visit_Program(self, node):
        print("visited -> Program")
        self.visit(node.content)

    def visit_StatementList(self, node):
        print("visited -> StatementList")
        for statement in node.content:
            self.visit(statement)
    
    def visit_Expression(self, node):
        pass

    def visit_SimpleStatement(self, node):
        pass

    def visit_AssignStatement(self, node):
        print("visited -> AssignStatement")
        self.visit(node.left)
        self.visit(node.right)

    def visit_If(self, node):
        pass

    def visit_While(self, node):
        pass

    def visit_For(self, node):
        pass

    def visit_Return(self, node):
        pass

    def visit_Control(self, node):
        pass

    def visit_ExpressionList(self, node):
        pass

    def visit_Identifier(self, node):
        print("visitd -> Identifier")

    def visit_Numericek(self, node):
        print("visitd -> Numericek")
        

    def visit_String(self, node):
        pass

    def visit_Vector(self, node):
        pass

    def visit_Matrix(self, node):
        pass

    def visit_FunctionCall(self, node):
        pass

    def visit_BinOp(self, node):
        pass

    def visit_UnaryOp(self, node):
        pass