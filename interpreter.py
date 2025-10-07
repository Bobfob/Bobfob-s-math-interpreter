from parser_ import *

def factorial(n: int) -> int:
    if isinstance(n, float): raise TypeError(f'Expected type \'int\', but got \'{type(n).__name__}\'')
    
    elif n < 0: raise ValueError("Expected n >= 0")
    
    elif n == 0: return 1
    
    else: return factorial(n - 1) * n

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
    
    def visit_FunctionCall(self, tree: FunctionCall):
        if tree.name in RESERVED_FUNCTIONS:
            ...
        
        else:
            raise Exception(f"Invalid name of a function: '{tree.name}'")
    
    def visit_IdentNode(self, tree: IdentNode):
        try: return self.defined_identifier[tree.ident][0]
        
        except KeyError: raise _InterpreterError(f'Undefined identifier: \'{tree.ident}\'')
