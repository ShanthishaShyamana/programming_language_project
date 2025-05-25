import sys
import re
from dataclasses import dataclass
from parser import Parser

@dataclass
class Token:
    type: str
    value: str

    def __str__(self):
        return f"<{self.type}:{self.value}>"

# Define keywords for RPAL
KEYWORDS = {
    'let', 'in', 'fn', 'where', 'rec', 'and', 'within',
    'aug', 'or', 'not', 'gr', 'ge', 'ls', 'le', 'eq', 'ne',
    'true', 'false', 'nil', 'dummy','@', '&', '|'
}

# Token specifications in priority order
token_specification = [
    ('COMMENT', r'//.*'),
    ('SKIP', r'[ \t\r\n]+'),
    ('STRING', r"'(\\'|\\\\|\\t|\\n|[^'])*'"),
    ('IDENTIFIER', r'[A-Za-z][A-Za-z0-9_]*'),
    ('INTEGER', r'\d+'),
    ('OPERATOR', r'[\+\-\*\/<>&\.@:=~|$!#%^_\[\]{}\"‘\?]+'),
    ('PUNCTUATION', r'[(),;]'),
    ('MISMATCH', r'.'),
]

token_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification))

def tokenize(code):

    tokens = []

    for match in token_re.finditer(code):
        kind = match.lastgroup
        value = match.group()

        if kind in {'SKIP', 'COMMENT'}:
            continue
        elif kind == 'IDENTIFIER':
            if value in KEYWORDS:
                tokens.append(Token("KEYWORD", value))
            else:
                tokens.append(Token("IDENTIFIER", value))
        elif kind == 'INTEGER':
            tokens.append(Token("INTEGER", value))
        elif kind == 'STRING':
            tokens.append(Token("STRING", value))
        elif kind == 'OPERATOR':
            tokens.append(Token("OPERATOR", value))
        elif kind == 'PUNCTUATION':
            tokens.append(Token("PUNCTUATION", value))
        elif kind == 'MISMATCH':
            raise RuntimeError(f"Unexpected character: {value}")
    return tokens

def main():
    if len(sys.argv) < 3 or sys.argv[1] != '-ast':
        print("Usage: python myrpal.py -ast file_name")
        sys.exit(1)

    filename = sys.argv[2]
    with open(filename, 'r') as f:
        code = f.read()

    tokens = tokenize(code)
    # Print tokens for debugging
    # for token in tokens:
    #     print(token)

    # for i in range(len(tokens)):
    #     print(f"{i}: {tokens[i]}")
    
    parser_instance = Parser(tokens)
    parser_instance.parse_E()  # Start parsing from the root rule

    # Now print AST
    stack = parser_instance.get_stack()
    print_ast(stack[-1])  # stack[-1] is the root of the AST


def print_ast(node, indent=0):
    print('.' * indent + node.type if node.value is None else f"{'.' * indent}<{node.type}:{node.value}>")
    for child in reversed(node.child):  # Print in reverse to maintain correct order
        print_ast(child, indent + 1)

# def main():
#     if len(sys.argv) < 2:
#         print("Usage: python myrpal.py file_name")
#         sys.exit(1)

#     filename = sys.argv[1]
#     with open(filename, 'r') as f:
#         code = f.read()

#     tokens = tokenize(code)
#     # for token in tokens:
#     #     print(token)

#     # Initialize the parser with the tokens
#       # Make sure your Parser class is defined in parser.py

#     # print(" Parser: Initializing")
#     parser_instance = Parser(tokens)


#     while True:
#         token = parser_instance.read()
#         if token is None:
#             break
    
    # print stack
  

    


if __name__ == "__main__":
    main()
