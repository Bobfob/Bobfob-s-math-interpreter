from lexer import Lexer
from parser_ import Parser
from interpreter import Interpreter
from os import system

def main():
    _print_tokens = False
    _print_tree   = False
    
    while (src := input('> Input: ')) != '.q':
        try:
            if src == '.clr':
                system('cls')
                continue
            
            elif src.split()[0].strip() == '.tokens':
                flags = src.split()
                
                if len(flags) == 2 and flags[1].strip() == '-t':
                    _print_tokens = True
                
                elif len(flags) == 2 and flags[1].strip() == '-f':
                    _print_tokens = False
                
                else:
                    print("Invalid flag")
                
                continue
            
            elif src.split()[0].strip() == '.tree':
                flags = src.split()
                
                if len(flags) == 2 and flags[1].strip() == '-t':
                    _print_tree = True
                
                elif len(flags) == 2 and flags[1].strip() == '-f':
                    _print_tree = False
                
                else:
                    print("Invalid flag")
                
                continue
            
            lex = Lexer(src)
            tokens = lex.tokenize()
            
            if _print_tokens:
                print('\nTokens: [')
                for token in tokens[:-1]:
                    print('  ', token, ',')
                print('  ', tokens[-1])
                print(']')

            par = Parser(tokens)
            tree = par.parse()
            
            if _print_tree:
                print('\nTree: ', tree, end='\n\n')

            int_ = Interpreter(tree)
            evaluated = int_.eval()
            print('> Output:', evaluated, '\n')
        
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
    print('\n[Program finished]')
