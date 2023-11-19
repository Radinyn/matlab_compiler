from sys import argv, stderr
from lech import Lech
from patryk import Patryk

if __name__ == '__main__':
    if len(argv) <= 1:
        print("No source file specified\nUsage: python3 main.py <source file>", file=stderr)
        exit(1) 
    
    filename = argv[1]
    try:
        source_file = open(filename, "r")
    except IOError:
        print(f"Cannot open \"{filename}\"", file=stderr)
        exit(1)

    text = source_file.read()

    lexer = Lech()
    tokens = lexer.tokenize(text)

    parser = Patryk()
    # x = parser.parse(tokens)

    parser.print_ast(tokens)
   

