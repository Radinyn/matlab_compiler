from sly import Lexer
from sly.lex import Token
from sys import stderr

class Lech(Lexer):
    identifiers = {ID}
    keywords = {
        IF,
        ELSE,
        FOR,
        WHILE,
        BREAK,
        CONTINUE,
        RETURN,
        EYE,
        ZEROS,
        ONES,
        PRINT,
    }
    operators = {
        PLUS,
        MINUS,
        TIMES,
        DIVIDE,
        ASSIGN,
        EQUAL,
        NOT_EQUAL,
        GREATER,
        LESS,
        GREATER_EQUAL,
        LESS_EQUAL,
        AND,
        OR,
        XOR,
        PLUS_ASSIGN,
        MINUS_ASSIGN,
        TIMES_ASSIGN,
        DIVIDE_ASSIGN,
        DOT_PLUS,
        DOT_MINUS,
        DOT_TIMES,
        DOT_DIVIDE,
        TRANSPOSE,
        RANGE,
    }
    builtin_types = { INTEGER, FLOAT, STRING }

    # Tokens
    tokens = { *identifiers, *operators, *keywords, *builtin_types }

    # Literals
    literals = {"(", ")", "{", "}", "[", "]", ";", ","}

    # String containing ignored characters between tokens
    ignore = " \t"
    ignore_newline = "\#.*"
    ignore_comment = "\n+"

    # Identifiers
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"

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
    PLUS_ASSIGN = r"\+="
    MINUS_ASSIGN = r"-="
    TIMES_ASSIGN = r"\*="
    DIVIDE_ASSIGN = r"/="

    DOT_PLUS = r"\.\+"
    DOT_MINUS = r"\.-"
    DOT_TIMES = r"\.\*"
    DOT_DIVIDE = r"\./"

    EQUAL = r"=="
    NOT_EQUAL = r"!="
    GREATER_EQUAL = r">="
    LESS_EQUAL = r"<="
    GREATER = r">"
    LESS = r"<"

    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"
    ASSIGN = r"="

    TRANSPOSE = r"'"
    RANGE = r":"

    @_(r'(\d+\.\d*|\.\d+)([Ee][\+-]?\d+)?')
    def FLOAT(self, token: Token) -> Token:
        token.value = float(token.value)
        return token

    @_(r'\d+')
    def INTEGER(self, token: Token) -> Token:
        token.value = int(token.value)
        return token

    @_(r'\"[^"]*\"')
    def STRING(self, token: Token) -> Token:
        token.value = str(token.value)
        return token


    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at {self.lineno}", file=stderr)
        self.index += 1


if __name__ == "__main__":
    lexer = Lech()
    while True:
        try:
            text = input("Lexer> ")
            print(list(lexer.tokenize(text)))
        except EOFError:
            break
