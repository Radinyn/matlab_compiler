from dataclasses import dataclass
from typing import Literal, Optional

Operator = Literal[
    "DOT_PLUS",
    "DOT_MINUS",
    "DOT_TIMES",
    "DOT_DIVIDE",
    "EQUAL",
    "NOT_EQUAL",
    "GREATER_EQUAL",
    "LESS_EQUAL",
    "GREATER",
    "LESS",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "TRANSPOSE",
    "RANGE",
    "SUBSCRIPT",
    ]

AssignOperator = Literal[
    "ASSIGN",
    "PLUS_ASSIGN",
    "MINUS_ASSIGN",
    "TIMES_ASSIGN",
    "DIVIDE_ASSIGN",
]

class Abraham:

    @dataclass
    class Node:
        pass

    @dataclass
    class Statement(Node):
        pass

    @dataclass
    class StatementList(Node):
        content: list['Abraham.Statement']

    @dataclass
    class Expression(Statement):
        pass

    @dataclass
    class SimpleStatement(Statement):
        value: 'Abraham.Expression'

    @dataclass
    class AssignStatement(Statement):
        left: 'Abraham.Expression'
        right: 'Abraham.Expression'
        operator: AssignOperator

    @dataclass
    class If(Statement):
        condition: 'Abraham.Expression'
        block: 'Abraham.StatementList'
        else_block: Optional['Abraham.StatementList']
    
    @dataclass
    class While(Statement):
        condition: 'Abraham.Expression'
        block: 'Abraham.StatementList'

    @dataclass
    class For(Statement):
        iterator: 'Abraham.Identifier'
        range: 'Abraham.Expression'
        block: 'Abraham.StatementList'

    @dataclass
    class Return(Statement):
        value: 'Abraham.Expression'

    @dataclass
    class Control(Statement):
        type: Literal["BREAK", "CONTINUE"]

    @dataclass
    class ExpressionList(Node):
        content: list['Abraham.Expression']

    @dataclass
    class Identifier(Expression):
        name: str

    @dataclass
    class Numericek(Expression):
        value: float | int

    @dataclass
    class String(Expression):
        value: str

    @dataclass
    class Vector(Expression):
        content: 'Abraham.ExpressionList'

    @dataclass
    class Matrix(Expression):
        rows: list['Abraham.Vector']

    @dataclass
    class FunctionCall(Expression):
        name: str
        arguments: 'Abraham.ExpressionList'

    @dataclass
    class BinOp(Expression):
        left: 'Abraham.Expression'
        right: 'Abraham.Expression'
        operator: Operator

    @dataclass
    class UnaryOp(Expression):
        operand: 'Abraham.Expression'
        operator: Operator




