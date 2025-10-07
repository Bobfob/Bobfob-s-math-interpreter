from lexer import Lexer
from parser_ import Parser
from interpreter import Interpreter

def main():
    while (src := input('> Input: ')) != '.q':
        try:
            lex = Lexer(src)
            tokens = lex.tokenize()
            print(tokens)

            par = Parser(tokens)
            tree = par.parse()
            print(tree)

            # int_ = Interpreter(tree)
            # evaluated = int_.eval()
            # print('> Output:', evaluated)
        
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
    print('\n[Program finished]')
