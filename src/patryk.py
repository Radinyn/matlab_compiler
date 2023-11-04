from sly import Parser
from sly.yacc import YaccProduction as Production
from lech import Lech

# ================================= Expected grammar =================================

# start -> program
# program -> statement
#
# statement -> statement_list
#            | expression;
#            | PRINT expression;
#            | assign_statement
#            | control_statement
#            | loop_statement
#            | empty_statement
#
# expression -> ( expression )
#             | expression PLUS           expression
#             | expression MINUS          expression
#             | expression TIMES          expression
#             | expression DIVIDE         expression
#             | expression DOT_PLUS       expression
#             | expression DOT_MINUS      expression
#             | expression DOT_TIMES      expression
#             | expression DOT_DIVIDE     expression
#             | expression EQUAL          expression
#             | expression NOT_EQUAL      expression
#             | expression GREATER        expression
#             | expression GREATER_EQUAL  expression
#             | expression LESS           expression
#             | expression LESS_EQUAL     expression
#             | FLOAT
#             | INTEGER
#
# statement_list ->  { statement_list } | statement_list statement | statement
#
# assign_statement -> expression ASSIGN expression;
#                   | expression PLUS_ASSIGN expression;
#                   | expression MINUS_ASSIGN expression;
#                   | expression TIMES_ASSIGN expression;
#                   | expression DIVIDE_ASSIGN expression;
# 
# control_statement -> IF ( expression ) statement
#                    | IF ( expression ) statement ELSE statement
# 
# loop_statement -> WHILE ( expression ) { statement }

class Patryk(Parser):
    tokens = Lech.tokens

    precedence = (
        ('right', ASSIGN, PLUS_ASSIGN, MINUS_ASSIGN, TIMES_ASSIGN, DIVIDE_ASSIGN, REMAINDER_ASSIGN),
        ('left', EQUAL, NOT_EQUAL, GREATER, GREATER_EQUAL, LOWER, LOWER_EQUAL),
        ('left', PLUS, MINUS, DOT_PLUS, DOT_MINUS),
        ('left', TIMES, DIVIDE, DOT_TIMES, DOT_DIVIDE),
        ('right', UNARY_MINUS),
        ('left', TRANSPOSE),
        ('nonassoc', NO_ELSE),
        ('nonassoc', ELSE)
    )

    start = 'program'

    # Program

    @_('program statement')
    def program(self, p: Production) -> Production:
        return p
    
    # Expressions
    
    @_(
            '"(" expression ")"',
            'expression PLUS          expression',
            'expression MINUS         expression',
            'expression TIMES         expression',
            'expression DIVIDE        expression',
            'expression DOT_PLUS      expression',
            'expression DOT_MINUS     expression',
            'expression DOT_TIMES     expression',
            'expression DOT_DIVIDE    expression',
            'expression EQUAL         expression',
            'expression NOT_EQUAL     expression',
            'expression GREATER       expression',
            'expression GREATER_EQUAL expression',
            'expression LESS          expression',
            'expression LESS_EQUAL    expression',
            'FLOAT',
            'INTEGER',
            'STRING',
            'ID'
    )
    def expression(self, p: Production) -> Production:
        return p
    
    @_('MINUS expression %prec UNARY_MINUS')
    def expression(self, p: Production) -> Production:
        return p
    
    # Statements
    
    @_('expression ";"')
    def statement(self, p: Production) -> Production:
        return p
    
    @_(
        'PRINT expression  ";"',
        'RETURN expression ";"'
    )
    def statement(self, p: Production) -> Production:
        return p
    
    @_(
        'expression ASSIGN          expression ";"',
        'expression PLUS_ASSIGN     expression ";"',
        'expression MINUS_ASSIGN    expression ";"',
        'expression TIMES_ASSIGN    expression ";"',
        'expression DIVIDE_ASSIGN   expression ";"',
    )
    def statement(self, p: Production) -> Production:
        return p


    @_(
        'IF "(" expression ")" statement %prec NO_ELSE',
        'IF "(" expression ")" statement ELSE statement',
    )
    def statement(self, p: Production) -> Production:
        return p
    
    @_('WHILE "(" expression ")" { statement }')
    def statement(self, p: Production) -> Production:
        return p
    
    @_('statement')
    def statement_list(self, p: Production) -> Production:
        return p
    
    @_('"{" statement_list "}"')
    def statement_list(self, p: Production) -> Production:
        return p
    
    @_('statement_list statement')
    def statement_list(self, p: Production) -> Production:
        return p