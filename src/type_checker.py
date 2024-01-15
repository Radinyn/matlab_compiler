from abraham import Abraham
from symbol_table import Symbol, SymbolTable
from visitor import NodeVisitor

class TypeChecker(NodeVisitor):
    symbol_table: SymbolTable

    def __init__(self):
        self.symbol_table = SymbolTable(parent=None, name=None)

    errors_total: int = 0
    
    def error(self, message: str) -> None:
        print(f"SyntaxError: {message}")
        self.errors_total += 1

    def check(self, ast_root) -> None:
        self.errors_total = 0
        self.visit(ast_root)
        print(f"Found {self.errors_total} syntax errors.")


    def visit_AssignStatement(self, node):
        # Now this is bad :pepew:
        right = self.visit(node.right)
        if right is None:
            self.error("Right side can not be assigned because of unknown type")
            return

        is_identifier = isinstance(node.left, Abraham.Identifier)
        is_subscript = isinstance(node.left, Abraham.BinOp) and node.left.operator == "SUBSCRIPT"

        if not is_identifier and not is_subscript:
            self.error("Left side of assign operator must be an l-value.")
            return

        id_name = node.left.name if is_identifier else node.left.left.name
        if self.symbol_table.get(id_name) is None and node.operator == "=":
            self.symbol_table.put(id_name, Symbol(right.type, right.shape))

        left = self.visit(node.left)
        if left != right:
            self.error("Left and right sides of an operator have different types or shapes")

    def visit_If(self, node):
        self.symbol_table = self.symbol_table.push_context("if")
        self.visit(node.block)
        self.symbol_table = self.symbol_table.pop_context()

    def visit_While(self, node):
        self.symbol_table = self.symbol_table.push_context("while")
        self.visit(node.block)
        self.symbol_table = self.symbol_table.pop_context()

    def visit_For(self, node):
        self.symbol_table = self.symbol_table.push_context("for")
        self.symbol_table.put(node.iterator, Symbol(type="int", shape=(1, )))
        self.visit(node.block)
        self.symbol_table = self.symbol_table.pop_context()

    def visit_Control(self, node):
        if not self.symbol_table.is_looping():
            self.error("Control statement outside of a loop")

    def visit_Identifier(self, node):
        node_type = self.symbol_table.get(node.name)
        if node_type  is None:
            self.error(f"Unknown identifier {node.name}")
        return node_type        

    def visit_BinOp(self, node):
        symbol_left = self.visit(node.left)
        symbol_right = self.visit(node.right)
        if symbol_left is None or symbol_right is None:
            self.error(" Binary operation not possible when one side has an unknown type")
            return None

        # TODO: A somewhat ugly solution
        if node.operator in [".+", ".-", ".*", "./", "==", "!=", "+", "-"]:
            if symbol_left != symbol_right:
                self.error("Left and right symbols must the same equal types")
                return None
            return symbol_left

        if node.operator in ["*"]:
            if symbol_left.type != symbol_right.type:
                self.error("Left and right sides of multiplication must have the same type")
                return None
            if symbol_left.shape[-1] != symbol_right.shape[0]:
                self.error("Incompatible shapes for multiplication")
                return None
            return Symbol(type=symbol_left.type, shape=(symbol_left.shape[0], symbol_right.shape[-1]))

        if node.operator in [">=", ">", "<", "<=", "/"]:
            if symbol_left.shape != (1, ) or symbol_right.shape != (1, ):
                self.error("Shape must be (1, ) for numerical comparison or division")
                return None
            return Symbol(type="bool", shape=(1, ))

        if node.operator in ["and", "or", "xor"]:
            if symbol_right.type != "bool" or symbol_left.type != "bool":
                self.error("Expected bool type on both sides of the logical operator")
                return None
            return Symbol(type="bool", shape=(1, ))

        if node.operator == "SUBSCRIPT":
            if not isinstance(node.left, Abraham.Identifier):
                self.error("Subscript mus have and identifier to it' left")
                return None
            id = self.visit(node.left)
            return Symbol(type=id.type, shape=(1, ))
 
    def visit_UnaryOp(self, node):
        symbol =  self.visit(node.operand)
        if node.operator == "'":
            return Symbol(type=symbol.type, shape=symbol.shape[::-1])
        return symbol

    def visit_ExpressionList(self, node):
        base_type = self.visit(node.content[0])
        for child in node.content:
            child_type = self.visit(child)
            if child_type != base_type:
                self.error(f"Different types of arguments in expression list")
                return None

        return Symbol(type=base_type.type, shape=(len(node.content), *base_type.shape))

    def visit_Numericek(self, node):
        value_type = "float" if isinstance(node.value, float) else "int"
        return Symbol(type=value_type, shape=(1, ))

    def visit_String(self, node):
        return Symbol(type="string", shape=(1, ))

    def visit_Vector(self, node):
        return self.visit(node.content)

    def visit_FunctionCall(self, node):
        # This is forced by our course. 
        # Since functions are grammar-defined their arguments are always an expression list with only one number.
        if node.name == "print":
            return None
    
        self.visit(node.arguments)
        args = node.arguments.content

        if len(args) != 1:
            self.error("Incorrect arguments.")
            return None
        size, symbol = args[0].value, self.visit(args[0])
        if symbol.type != "int":
            self.error("Size must be an integer")
            return None

        return Symbol(type="float", shape = (size, size))
