from abraham import Abraham
from symbol_table import Symbol, SymbolTable

class NodeVisitor(object):
    symbol_table: SymbolTable

    def __init__(self):
        self.symbol_table = SymbolTable(parent=None, name=None)

    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        print(method)
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


class TypeChecker(NodeVisitor):

    def check(self, ast_root) -> None:
        self.visit(ast_root)
        # print(self.symbol_table.lookup)


    def visit_AssignStatement(self, node):
        right = self.visit(node.right)

        if right is None:
            print("[ERROR] Right side can not be assigned")
            return

        if not isinstance(node.left, Abraham.Identifier):
            print(f"[ERROR] Left side of assign operator must be an l-value.")
            return

        if self.symbol_table.get(node.left.name) is None and node.operator == "=":
            self.symbol_table.put(node.left.name, Symbol(right.type, right.shape))

        left = self.visit(node.left)
        if left != right:
            print("[ERROR] Left and right sides of an operator have different types or shapes")


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
        self.visit(node.block)
        self.symbol_table = self.symbol_table.pop_context()

    def visit_Control(self, node):
        if not self.symbol_table.is_looping():
            print("[ERROR] Control statement outside of a loop")

    def visit_Identifier(self, node):
        node_type = self.symbol_table.get(node.name)
        if node_type  is None:
            print(f"[ERROR] Unknown identifier {node.name}")
        return node_type        

    def visit_BinOp(self, node):
        symbol_left = self.visit(node.left)
        symbol_right = self.visit(node.right)
        if symbol_left is None or symbol_right is None:
            print("[ERROR] Binary operation not possible when one side has an unknown type")
            return None

        # TODO: A somewhat ugly solution
        if node.operator in [".+", ".-", ".*", "./", "==", "!=", "+", "-"]:
            if symbol_left != symbol_right:
                print("[ERROR] Left and right symbols must the same equal types")
                return None
            return symbol_left

        if node.operator in ["*"]:
            if symbol_left.type != symbol_right.type:
                print("[ERROR] Left and right sides of multiplication must have the same type")
                return None
            if symbol_left.shape[-1] != symbol_right.shape[0]:
                print("[ERROR] Incompatible shapes for multiplication")
                return None
            return Symbol(type=symbol_left.type, shape=(symbol_left.shape[0], symbol_right.shape[-1]))

        if node.operator in [">=", ">", "<", "<=", "/"]:
            if symbol_left.shape != (1, ) or symbol_right.shape != (1, ):
                print("[ERROR] Shape must be (1, ) for numerical comparison or division")
                return None
            return Symbol(type="bool", shape=(1, ))

        if node.operator in ["and", "or", "xor"]:
            if symbol_right.type != "bool" or symbol_left.type != "bool":
                print("[ERROR] Expected bool type on both sides of the logical operator")
                return None
            return Symbol(type="bool", shape=(1, ))
 
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
                print(f"[ERROR] Different types of arguments in expression list")
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
        self.visit(node.arguments)
        args = node.arguments.content
        if len(args) != 1:
            print("[ERROR] Incorrect arguments.")
            return None

        size, symbol = args[0].value, self.visit(args[0])
        if symbol.type != "int":
            print("[ERROR] Size must be an integer")
            return None

        return Symbol(type="float", shape = (size, size))
