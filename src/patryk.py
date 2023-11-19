from sys import stderr
from sly import Parser
from sly.yacc import YaccProduction as Production
from lech import Lech
from abraham import Abraham
from sly.lex import Token
from pprint import pprint
from dataclasses import asdict

class Patryk(Parser):
    tokens = Lech.tokens

    debugfile = 'parser.out'

    precedence = (
        ('right', ASSIGN, PLUS_ASSIGN, MINUS_ASSIGN, TIMES_ASSIGN, DIVIDE_ASSIGN),
        ('nonassoc', RANGE),
        ('left', AND, OR, XOR),
        ('left', EQUAL, NOT_EQUAL, GREATER, GREATER_EQUAL, LESS, LESS_EQUAL),
        ('left', PLUS, MINUS, DOT_PLUS, DOT_MINUS),
        ('left', TIMES, DIVIDE, DOT_TIMES, DOT_DIVIDE),
        ('right', UNARY_MINUS),
        ('left', TRANSPOSE),
        ('left', SUBSCRIPT),
        ('nonassoc', NO_ELSE),
        ('nonassoc', ELSE)
    )

    # ====== Program ======
    
    start = 'program'

    @_('statement_list')
    def program(self, p: Production):
        return p

    # ====== Expressions ======

    # Binary arythmetic expressions
    @_(
        '"(" expression ")"',
        'expression PLUS          expression',
        'expression MINUS         expression',
        'expression TIMES         expression',
        'expression DIVIDE        expression',
        'expression DOT_PLUS      expression',
        'expression DOT_MINUS     expression',
        'expression DOT_TIMES     expression',
        'expression DOT_DIVIDE    expression'
    )
    def expression(self, p: Production) -> Production:
        return Abraham.BinOp(
            left=p[0],
            right=p[2],
            operator=p[1],
        )
    
    # Binary relation expressions
    @_(
        'expression EQUAL         expression',
        'expression NOT_EQUAL     expression',
        'expression GREATER       expression',
        'expression GREATER_EQUAL expression',
        'expression LESS          expression',
        'expression LESS_EQUAL    expression'
    )
    def expression(self, p: Production) -> Production:
        return Abraham.BinOp(
            left=p[0],
            right=p[2],
            operator=p[1],
        )

    # Binary logical expression
    @_(
        'expression AND expression',
        'expression OR  expression',
        'expression XOR expression',
    )
    def expression(self, p: Production) -> Production:
        return Abraham.BinOp(
            left=p[0],
            right=p[2],
            operator=p[1],
        )

    # Value expressions
    @_('FLOAT')
    def expression(self, p: Production) -> Production:
        return Abraham.Numericek(value=float(p[0]))
    
    @_('INTEGER')
    def expression(self, p: Production) -> Production:
        return Abraham.Numericek(value=int(p[0]))
    
    @_('STRING')
    def expression(self, p: Production) -> Production:
        return Abraham.String(value=str(p[0]))
    
    @_('ID')
    def expression(self, p: Production) -> Production:
        return Abraham.Identifier(name=str(p[0]))
    
    # Unary operators
    @_('MINUS expression %prec UNARY_MINUS')
    def expression(self, p: Production) -> Production:
        return Abraham.UnaryOp(
            operand=p[1],
            operator=p[0],
        )
    
    @_('expression TRANSPOSE %prec TRANSPOSE')
    def expression(self, p: Production) -> Production:
        return Abraham.UnaryOp(
            operand=p[1],
            operator=p[0],
        )

    # Range operator
    @_('expression RANGE expression')
    def expression(self, p: Production) -> Production:
        return Abraham.BinOp(
            left=p[0],
            right=p[2],
            operator=p[1],
        )

    # Built-in functions
    @_('EYE   "(" expression ")"',
       'ZEROS "(" expression ")"',
       'ONES  "(" expression ")"')
    def expression(self, p: Production) -> Production:
        return Abraham.FunctionCall(
            name=p[0],
            arguments=Abraham.ExpressionList(
                content=[p[2]]
            )
        )

    # Subscript
    @_('expression "[" expression_list "]" %prec SUBSCRIPT')
    def expression(self, p: Production) -> Production:
        return Abraham.BinOp(
            left=p[0],
            right=p[2],
            operator="SUBSCRIPT",
        )

    # ====== Expression list ======
    @_('expression')
    def expression_list(self, p: Production) -> Production:
        return Abraham.ExpressionList(content=[p[0]])
    
    @_('expression_list "," expression')
    def expression_list(self, p: Production) -> Production:
        return Abraham.ExpressionList(content=p[0].content + [p[2]])

    @_('')
    def expression_list(self, p: Production) -> Production:
        return Abraham.ExpressionList(content=[])

    # ====== Lists ======

    @_('"[" expression_list "]"')
    def vector(self, p: Production) -> Production:
        return Abraham.Vector(content=p[1])
    
    @_('vector')
    def expression(self, p: Production) -> Production:
        return p[0]
 
    # ====== Statements ======
    
    # Standalone expression
    @_('expression ";"')
    def statement(self, p: Production) -> Production:
        return p[0]
    
    # Loop control
    @_('BREAK ";"',
       'CONTINUE ";"')
    def statement(self, p: Production) -> Production:
        return Abraham.Control(type=p[0])
    
    # Built-in print
    @_('PRINT "(" expression_list ")" ";"')
    def statement(self, p: Production) -> Production:
        return Abraham.FunctionCall(
            name=p[0],
            arguments=p[2],
        )

    # Return statements
    @_('RETURN expression ";"')
    def statement(self, p: Production) -> Production:
        return Abraham.Return(value=p[1])
    
    # Assignments
    @_(
        'expression ASSIGN          expression ";"',
        'expression PLUS_ASSIGN     expression ";"',
        'expression MINUS_ASSIGN    expression ";"',
        'expression TIMES_ASSIGN    expression ";"',
        'expression DIVIDE_ASSIGN   expression ";"',
    )
    def statement(self, p: Production) -> Production:
        return Abraham.AssignStatement(
            left=p[0],
            right=p[2],
            operator=p[1],
        )

    # Control statements
    @_(
        'IF "(" expression ")" statement %prec NO_ELSE',
    )
    def statement(self, p: Production) -> Production:
        return Abraham.If(
            condition=p[2],
            block=p[4],
            else_block=None,
        )
    
    @_(
        'IF "(" expression ")" statement ELSE statement',
    )
    def statement(self, p: Production) -> Production:
        return Abraham.If(
            condition=p[2],
            block=p[4],
            else_block=p[6],
        )
    
    # Loops
    @_('WHILE "(" expression ")" statement')
    def statement(self, p: Production) -> Production:
        return Abraham.While(
            condition=p[2],
            block=p[4],
        )
    
    @_('FOR "(" ID ASSIGN expression ")" statement')
    def statement(self, p: Production) -> Production:
        return Abraham.For(
            iterator=p[2],
            range=p[4],
            block=p[6],
        )

    # ====== Statement List ======
    @_('"{" statement_list "}"')
    def statement(self, p: Production):
        if isinstance(p[1], Abraham.StatementList):
            return p[1]
        else:
            return Abraham.StatementList(content=[p[1]])

    @_('statement')
    def statement_list(self, p: Production):
        if isinstance(p[0], Abraham.StatementList):
            return p[0]
        else:
            return Abraham.StatementList(content=[p[0]])
    
    @_('statement_list statement')
    def statement_list(self, p: Production):
        list0 = p[0].content if isinstance(p[0], Abraham.StatementList) else [p[0]]
        list1 = p[1].content if isinstance(p[1], Abraham.StatementList) else [p[1]]
        return Abraham.StatementList(content=list0+list1)
    
    def error(self, token: Token) -> None:
        if not token:
            print("SyntaxError: End of file reached", file = stderr)
            return
    
        print(f"SyntaxError: Invalid token {token.type} at line {token.lineno}", file = stderr)


    def get_ast(self, tokens):
        parsed = self.parse(tokens)
        return parsed[1]
    
    def print_ast(self, tokens, hide_names = False):
        ast = self.get_ast(tokens)
        if hide_names:
            ast = asdict(ast)
        pprint(ast, width=1, indent=1)
