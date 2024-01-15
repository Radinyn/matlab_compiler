from visitor import NodeVisitor
from memory import Memory, MemoryStack
import numpy as np
from control_statements import ReturnException, BreakException, ContinueException

class Interpreter(NodeVisitor):
    def __init__(self):
        self.memory_stack = MemoryStack(Memory(name="global"))

    def error(self, message: str) -> None:
        print(f"RuntimeError: {message}")

    def interpret(self, root):
        self.visit(root)
        print("\nMemory dump:")
        self.memory_stack.dump_memory()

    def visit_AssignStatement(self, node):
        name = node.left.name
        value = self.visit(node.right)
        if node.operator == "=":
            self.memory_stack.insert(name, value)
            return
        
        original = self.memory_stack.get(name)
        if node.operator == "+=":
            self.memory_stack.insert(name, original + value)
        if node.operator == "-=":        
            self.memory_stack.insert(name, original - value)
        if node.operator == "*=":        
            self.memory_stack.insert(name, original * value)
        if node.operator == "/=":        
            self.memory_stack.insert(name, original / value)

    def visit_If(self, node):
        self.memory_stack.push(Memory(name="if"))
        try:
            if self.visit(node.condition):
                self.visit(node.block)
            elif node.else_block is not None: 
                self.visit(node.else_block)
        except (BreakException, ContinueException) as e:
            self.memory_stack.pop()
            raise e
        self.memory_stack.pop()
    
    def visit_While(self, node):
        self.memory_stack.push(Memory(name="while"))
        while self.visit(node.condition):
            try:
                self.visit(node.block)
            except BreakException:
                break
            except ContinueException:
                continue    
        self.memory_stack.pop()

    def visit_For(self, node):
        self.memory_stack.push(Memory(name="for"))
        for i in self.visit(node.range):
            try:
                self.memory_stack.insert(node.iterator, i)
                self.visit(node.block)
            except BreakException:
                break
            except ContinueException:
                continue    
        self.memory_stack.pop()

    def visit_Return(self, node):
        raise ReturnException(self.visit(node.right))

    def visit_Control(self, node):
        if node.type == "break":
            raise BreakException()
        if node.type == "continue":
            raise ContinueException()

    def visit_ExpressionList(self, node):
        # content: list['Abraham.Expression']
        pass

    def visit_Identifier(self, node):
        return self.memory_stack.get(node.name)

    def visit_Numericek(self, node):
        # value: float | int
        return node.value

    def visit_String(self, node):
        return node.value[1:-1]

    def visit_Vector(self, node):
        return np.array([self.visit(elem) for elem in node.content.content])


    def visit_Matrix(self, node):
        return np.concatenate([self.visit(v) for v in node.rows], axis=0)

    def visit_FunctionCall(self, node):
        if node.name == "print":
            print(self.visit(node.arguments.content[0]))
            return

        size = self.visit(node.arguments.content[0])
        match node.name:
            case "eye":
                return np.eye(size)
            case "ones":
                return np.ones((size, size))
            case "zeros":
                return np.zeros(size)



    def visit_BinOp(self, node):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        # Retarded solution
        match node.operator:
            case "+":
                return left_value + right_value
            case "-":
                return left_value - right_value
            case "*":
                return left_value @ right_value
            case "/":
                return left_value / right_value
            case ".+":
                return np.add(left_value, right_value)
            case ".-":
                return np.subtract(left_value, right_value)
            case ".*":
                return left_value * right_value
            case "./":
                return np.divide(left_value, right_value)
            case ">":
                return left_value > right_value
            case ">=":
                return left_value >= right_value
            case "<":
                return left_value < right_value
            case "<=":
                return left_value <= right_value
            case ":":
                return range(left_value, right_value)

    def visit_UnaryOp(self, node):
        # operand: 'Abraham.Expression'
        # operator: Operator
        pass
