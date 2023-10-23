
from sly import Lexer

class Lech(Lexer):
    identifiers = {ID}
    keywords = {IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN, EYE, ZEROS, ONES, PRINT}
    operators = {ADD, SUB, MUL, DIV, MOV, EQ, NEQ, GT, LT, GE, LE, IADD, ISUB, IMUL, IDIV, DADD, DSUB, DMUL, DDIV, TPOS, RANG}
    punctuation = {LPAR, RPAR, LSPAR, RSPAR, LCPAR, RCPAR, COMMA, SEMICOLON, COMMENT}
    types = {INT, FLOAT, STRING}

    tokens = {*identifiers, *types, *punctuation, *operators, *keywords}

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Identifiers
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Keywords
    ID["if"] = IF
    ID["else"] = ELSE
    ID["for"] = FOR
    ID["while"] = WHILE
    ID["break"] = BREAK
    ID["continue"] = CONTINUE
    ID["return"] = RETURN
    ID["eye"] = EYE
    ID["zeros"] = ZEROS
    ID["ones"] = ONES
    ID["print"] = PRINT    

    # Operators
    ADD = r'\+'
    SUB = r'-'
    MUL = r'\*'
    DIV = r'/'
    MOV = r'='

    EQ = r'=='
    NEQ = r'!='
    GT = r'>'
    LT = r'<'
    GE = r'>='
    LE = r'<='

    IADD = r'\+='
    ISUB = r'-='
    IMUL = r'\*='
    IDIV = r'/='

    DADD = r'\.\+'
    DSUB = r'\.-'
    DMUL = r'\.\*'
    DDIV = r'\./'

    TPOS = r"'"
    RANG = r':'

    # Punctuation
    LPAR = r'\('
    RPAR = r'\)'
    LSPAR = r'\['
    RSPAR = r'\]'
    LCPAR = r'{'
    RCPAR = r'}'
    COMMA = r','
    SEMICOLON = r';'
    COMMENT = r"#.*"

    # Types
    FLOAT = r'(\d*\.\d+|\d+\.\d*)([Ee][\+-]?\d+)?'
    INT = r'\d+'
    STRING = r'"([^"\\]*(\\.[^"\\]*)*)"'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at {self.lineno}")
        self.index += 1

if __name__ == '__main__':
    lexer = Lech()
    while True:
        try:
            text = input('input > ')
        except EOFError:
            break
        if text:
            print(list(lexer.tokenize(text)))
