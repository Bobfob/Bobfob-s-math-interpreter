from parser_ import *
import math

def factorial(n: int) -> int:
    if isinstance(n, float): raise TypeError(f'Expected type \'int\', but got \'{type(n).__name__}\'')
    
    elif n < 0: raise ValueError("Expected n >= 0")
    
    elif n == 0: return 1
    
    else: return factorial(n - 1) * n

class ReservedFunctions:
    @staticmethod
    def cos(x) -> float: return math.cos(x)
    @staticmethod
    def sin(x) -> float: return math.sin(x)
    @staticmethod
    def tan(x) -> float: return math.tan(x)
    @staticmethod
    def cot(x) -> float: return 1 / math.tan(x)
    @staticmethod
    def sec(x) -> float: return 1 / math.cos(x)
    @staticmethod
    def csc(x) -> float: return 1 / math.sin(x)
    @staticmethod
    def ln(x) -> float: return math.log(x)
    @staticmethod
    def log(x) -> float: return math.log10(x)
    @staticmethod
    def logn(x, base) -> float: return math.log(x, base)
    @staticmethod
    def exp(x) -> float: return math.exp(x)
    @staticmethod
    def abs(x) -> float: return abs(x)
    @staticmethod
    def ceil(x) -> float: return math.ceil(x)
    @staticmethod
    def floor(x) -> float: return math.floor(x)
    @staticmethod
    def cosh(x) -> float: return math.cosh(x)
    @staticmethod
    def sinh(x) -> float: return math.sinh(x)
    @staticmethod
    def tanh(x) -> float: return math.tanh(x)
    @staticmethod
    def coth(x) -> float: return 1 / math.tanh(x)
    @staticmethod
    def sech(x) -> float: return 1 / math.cosh(x)
    @staticmethod
    def csch(x) -> float: return 1 / math.sinh(x)
    @staticmethod
    def cos_d(x) -> float: return math.cos(math.radians(x))
    @staticmethod
    def sin_d(x) -> float: return math.sin(math.radians(x))
    @staticmethod
    def tan_d(x) -> float: return math.tan(math.radians(x))
    @staticmethod
    def cot_d(x) -> float: return 1 / math.tan(math.radians(x))
    @staticmethod
    def sec_d(x) -> float: return 1 / math.cos(math.radians(x))
    @staticmethod
    def csc_d(x) -> float: return 1 / math.sin(math.radians(x))
    @staticmethod
    def clamp(x, min_x, max_x) -> int | float: return min(max(x, min_x), max_x)
    @staticmethod
    def min(x, y, *args) -> int | float: return min(x, y, *args)
    @staticmethod
    def max(x, y, *args) -> int | float: return max(x, y, *args)

class _InterpreterError(Exception): ...

class Interpreter:
    def __init__(self, tree: ExprBase):
        self.tree = tree
        
        # desc: IDENT: ("value", "is_const")
        self.defined_identifier = {
            'pi':  (3.1415926535897932384626433832795, True),
            'e':   (2.7182818284590452353602874713527, True),
            'tau': (6.283185307179586476925286766559,  True)
        }
    
    def eval(self):
        return self.visit(self.tree)
    
    def visit(self, tree: ExprBase):
        visit_method_name = f'visit_{type(tree).__name__}'
        visit_method = getattr(self, visit_method_name)
        return visit_method(tree)
    
    def visit_PlusNode(self, tree: PlusNode):             return self.visit(tree.lhs) + self.visit(tree.rhs)
    
    def visit_MinusNode(self, tree: MinusNode):           return self.visit(tree.lhs) - self.visit(tree.rhs)
    
    def visit_MulNode(self, tree: MulNode):               return self.visit(tree.lhs) * self.visit(tree.rhs)
    
    def visit_DivNode(self, tree: DivNode):               return self.visit(tree.lhs) / self.visit(tree.rhs)
    
    def visit_PowerNode(self, tree: PowerNode):           return self.visit(tree.lhs) **self.visit(tree.rhs)
    
    def visit_ModNode(self, tree: ModNode):               return self.visit(tree.lhs) % self.visit(tree.rhs)
    
    def visit_UnaryPlusNode(self, tree: UnaryPlusNode):   return  self.visit(tree.value)
    
    def visit_UnaryMinusNode(self, tree: UnaryMinusNode): return -self.visit(tree.value)
    
    def visit_NumberNode(self, tree: NumberNode):         return tree.value
    
    def visit_FactorialNode(self, tree: FactorialNode):   return factorial(self.visit(tree.value))
    
    def evaluate_function_arguments(self, args: list[ExprBase]) -> list[Any]:
        return [self.visit(arg) for arg in args]
    
    def visit_FunctionCall(self, tree: FunctionCall):
        if tree.name in RESERVED_FUNCTIONS:
            func_args = self.evaluate_function_arguments(tree.args)
            cur_method = getattr(ReservedFunctions, tree.name)
            return cur_method(*func_args)
        
        else:
            raise Exception(f"Invalid name of a function: '{tree.name}'")
    
    def visit_IdentNode(self, tree: IdentNode):
        try: return self.defined_identifier[tree.ident][0]
        
        except KeyError: raise _InterpreterError(f'Undefined identifier: \'{tree.ident}\'')
