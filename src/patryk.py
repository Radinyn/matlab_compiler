from sys import stderr
from sly import Parser
from sly.yacc import YaccProduction as Production
from lech import Lech
from sly.lex import Token

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
        return p
    
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
        return p

    # Binary logical expression
    @_(
        'expression AND expression',
        'expression OR  expression',
        'expression XOR expression',
    )
    def expression(self, p: Production) -> Production:
        return p

    # Value expressions
    @_('FLOAT', 'INTEGER', 'STRING', 'ID')
    def expression(self, p: Production) -> Production:
        return p
    
    # Unary operators
    @_('MINUS expression %prec UNARY_MINUS')
    def expression(self, p: Production) -> Production:
        return p
    
    @_('expression TRANSPOSE %prec TRANSPOSE')
    def expression(self, p: Production) -> Production:
        return p

    # Range operator
    @_('expression RANGE expression')
    def expression(self, p: Production) -> Production:
        return p

    # Built-in functions
    @_('EYE   "(" expression ")"',
       'ZEROS "(" expression ")"',
       'ONES  "(" expression ")"')
    def expression(self, p: Production) -> Production:
        return p

    # Subscript
    @_('expression "[" expression_list "]" %prec SUBSCRIPT')
    def expression(self, p: Production) -> Production:
        return p

    # ====== Expression list ======
    @_('expression')
    def expression_list(self, p: Production) -> Production:
        return p
    
    @_('expression_list "," expression')
    def expression_list(self, p: Production) -> Production:
        return p

    @_('')
    def expression_list(self, p: Production) -> Production:
        return p

    # ====== Lists ======

    @_('"[" expression_list "]"')
    def vector(self, p: Production) -> Production:
        return p
    
    @_('vector')
    def expression(self, p: Production) -> Production:
        return p
 
    # ====== Statements ======
    
    # Standalone expression
    @_('expression ";"')
    def statement(self, p: Production) -> Production:
        return p
    
    # Loop control
    @_('BREAK ";"',
       'CONTINUE ";"')
    def statement(self, p: Production) -> Production:
        return p
    
    # Built-in print
    @_('PRINT "(" expression_list ")" ";"')
    def statement(self, p: Production) -> Production:
        return p

    # Return statements
    @_('RETURN expression ";"')
    def statement(self, p: Production) -> Production:
        return p
    
    # Assignments
    @_(
        'expression ASSIGN          expression ";"',
        'expression PLUS_ASSIGN     expression ";"',
        'expression MINUS_ASSIGN    expression ";"',
        'expression TIMES_ASSIGN    expression ";"',
        'expression DIVIDE_ASSIGN   expression ";"',
    )
    def statement(self, p: Production) -> Production:
        return p

    # Control statements
    @_(
        'IF "(" expression ")" statement %prec NO_ELSE',
        'IF "(" expression ")" statement ELSE statement',
    )
    def statement(self, p: Production) -> Production:
        return p
    
    # Loops
    @_('WHILE "(" expression ")" statement')
    def statement(self, p: Production) -> Production:
        return p
    
    @_('FOR "(" ID ASSIGN expression ")" statement')


    # ====== Statement List ======
    @_('"{" statement_list "}"')
    def statement(self, p: Production):
        return p

    @_('statement')
    def statement_list(self, p: Production):
        return p
    
    @_('statement_list statement')
    def statement_list(self, p: Production):
        return p
    
    def error(self, token: Token) -> None:
        if not token:
            print("SyntaxError: End of file reached", file = stderr)
            return
    
        print(f"SyntaxError: Invalid token {token.type} at line {token.lineno}", file = stderr)
