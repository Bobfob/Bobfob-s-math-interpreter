from tokens import *

class _LexerError(Exception): ...

class Lexer:
    def __init__(self, source: str):
        self.source = iter(source)
        self.source_lit = source
        self.index = -1

        self.advance()
    
    def advance(self):
        try:
            self.cur_char = next(self.source)
            self.index += 1
        except StopIteration:
            self.cur_char = None
    
    def peek(self, offset = 0):
        return self.source_lit[max(0, min(self.index + offset, len(self.source_lit) - 1))]
    
    def eat(self):
        prev = self.peek()
        self.advance()
        return prev

    def tokenize(self):
        result = []

        while self.cur_char != None:
            while self.cur_char.isspace():
                self.advance()
            
            # Numbers
            if self.cur_char.isdigit() or (self.cur_char == '.' and self.peek(1).isdigit()):
                number = ''
                dots = 0

                if self.cur_char == '.':
                    dots += 1
                    number += self.eat()
                
                while self.cur_char != None and (self.cur_char.isdigit() or self.cur_char == '.'):
                    if dots > 1:
                        raise _LexerError('Invalid number')

                    number += self.eat()
                    
                    if self.cur_char == '.':
                        dots += 1
                        number += self.eat()
                
                result.append(Token(TokenType.NumberLit, int(number) if dots == 0 else float(number)))
            
            # Identifiers
            elif self.cur_char.isalnum() or self.cur_char == '_':
                ident = ''

                while self.cur_char != None and (self.cur_char.isalnum() or self.cur_char == '_'):
                    ident += self.eat()
                
                result.append(Token(TokenType.Identifier, ident))
            
            else:
                match self.cur_char:
                    case '(': result.append(Token(TokenType.LParen, self.eat()))
                    case ')': result.append(Token(TokenType.RParen, self.eat()))
                    case '=': result.append(Token(TokenType.Assign, self.eat()))
                    case '!': result.append(Token(TokenType.PostfixOp, self.eat()))
                    case ',': result.append(Token(TokenType.Comma, self.eat()))
                    case '+': result.append(Token(TokenType.BinaryOp, self.eat()))
                    case '-': result.append(Token(TokenType.BinaryOp, self.eat()))
                    case '*':
                        if self.peek(1) == '*':
                            self.advance()
                            self.advance()
                            result.append(Token(TokenType.BinaryOp, '**'))
                        else:
                            result.append(Token(TokenType.BinaryOp, self.eat()))
                    case '/': result.append(Token(TokenType.BinaryOp, self.eat()))
                    case '%': result.append(Token(TokenType.BinaryOp, self.eat()))
                    case _:
                        self.advance()
                        # raise _LexerError(f'Invalid symbol: {self.cur_char}')
        
        return result
