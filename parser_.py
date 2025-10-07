from lexer import *
from nodes import *

RESERVED_FUNCTIONS = (
    "cos",   "sin",   "tan",
    "cot",   "sec",   "csc",
    "ln",    "log",   "logn",
    "exp",   "sqrt",  "cbrt",
    "abs",   "floor", "ceil",
    "cosh",  "sinh",  "tanh",
    "coth",  "sech",  "csch",
    "cos_d", "sin_d", "tan_d",
    "cot_d", "sec_d", "csc_d",
    "clamp", "min",   "max",
)

class _ParserError(Exception): ...

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = iter(tokens)
        self.tokens_lit = tokens
        self.index = -1

        self.advance()
    
    def advance(self):
        try:
            self.cur_token = next(self.tokens)
            self.index += 1
        except StopIteration:
            self.cur_token = None
    
    def peek(self, offset = 0):
        return self.tokens_lit[max(0, min(self.index + offset, len(self.tokens_lit) - 1))]

    def eat(self):
        prev = self.cur_token
        self.advance()
        return prev

    def expected(self, check: TokenType, explanation: str):
        if self.cur_token == None or self.cur_token.type != check:
            raise _ParserError(f"Expected '{explanation}'")
        
        self.advance()

    def parse(self) -> ExprBase:
        return self.parse_expr()

    def parse_expr(self) -> ExprBase:
        if self.cur_token == None:
            raise _ParserError('Invalid expression')
        
        result = self.parse_expr_tail()

        if self.cur_token != None:
            raise _ParserError('Invalid expression')
        
        return result

    def parse_function_call_args(self) -> list[ExprBase]:
        args: list[ExprBase] = []
        
        while self.cur_token != None and self.cur_token.type != TokenType.RParen:
            args.append(self.parse_expr_tail())
            
            if self.cur_token.type != TokenType.RParen:
                self.expected(TokenType.Comma, ',')
        
        return args
    
    def parse_expr_tail(self) -> ExprBase:
        lhs = self.parse_term()

        while self.cur_token != None and self.cur_token.type == TokenType.BinaryOp and self.cur_token.value in ('+', '-'):
            if self.cur_token.value == '+':
                self.advance()
                lhs = PlusNode(lhs, self.parse_term())
            
            elif self.cur_token.value == '-':
                self.advance()
                lhs = MinusNode(lhs, self.parse_term())
        
        return lhs

    def parse_term(self) -> ExprBase:
        lhs = self.parse_power()

        while self.cur_token != None and self.cur_token.type == TokenType.BinaryOp and self.cur_token.value in ('*', '/', '%'):
            if self.cur_token.value == '*':
                self.advance()
                lhs = MulNode(lhs, self.parse_power())
            
            elif self.cur_token.value == '/':
                self.advance()
                lhs = DivNode(lhs, self.parse_power())
            
            elif self.cur_token.value == '%':
                self.advance()
                lhs = ModNode(lhs, self.parse_power())
        
        return lhs

    def parse_power(self) -> ExprBase:
        lhs = self.parse_postfix()

        while self.cur_token != None and self.cur_token.type == TokenType.BinaryOp and self.cur_token.value == '**':
            self.advance()
            lhs = PowerNode(lhs, self.parse_postfix())
        
        return lhs
    
    def parse_postfix(self) -> ExprBase:
        lhs = self.parse_primary()
        
        while self.cur_token != None and self.cur_token.type == TokenType.PostfixOp and self.cur_token.value in ('!',):
            if self.cur_token.value == '!':
                self.advance()
                lhs = FactorialNode(lhs)
        
        return lhs
    
    def parse_primary(self) -> ExprBase:
        tok = self.cur_token

        if tok == None:
            raise _ParserError('Invalid expr')
        
        elif tok.type == TokenType.LParen:
            self.advance()
            result = self.parse_expr_tail()
            self.expected(TokenType.RParen, ')')
            return result
        
        elif tok.type == TokenType.NumberLit:
            self.advance()
            return NumberNode(tok.value) # type: ignore

        elif tok.type == TokenType.Identifier:
            name = tok.value
            self.advance()
            
            if self.cur_token != None and self.cur_token.type == TokenType.LParen:
                self.advance()
                args = self.parse_function_call_args()
                self.expected(TokenType.RParen, ')')
                
                if name not in RESERVED_FUNCTIONS:
                    raise _ParserError(f"Invalid function name: '{name}'")
                
                return FunctionCall(name, args)
            
            else:
                return IdentNode(name) # type: ignore

        elif tok.type == TokenType.BinaryOp:
            match tok.value:
                case '+':
                    self.advance()
                    return UnaryPlusNode(self.parse_primary())
                
                case '-':
                    self.advance()
                    return UnaryMinusNode(self.parse_primary())
        
        raise _ParserError("Invalid expr")
