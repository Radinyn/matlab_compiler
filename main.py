import sys
from lech import Lech


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "resources/example.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Lech()
    tokens = list(lexer.tokenize(text))
    print(*tokens, sep="\n")
