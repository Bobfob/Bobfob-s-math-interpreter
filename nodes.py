from tokens import dataclass

@dataclass
class ExprBase: ...

@dataclass
class PlusNode(ExprBase):
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self): return f"({self.lhs} + {self.rhs})"
@dataclass
class MinusNode(ExprBase):
    lhs: ExprBase
    rhs: ExprBase
    
    def __str__(self): return f"({self.lhs} - {self.rhs})"
@dataclass
class MulNode(ExprBase):
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self): return f"({self.lhs} * {self.rhs})"
@dataclass
class PowerNode(ExprBase):
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self): return f"({self.lhs} ** {self.rhs})"
@dataclass
class DivNode(ExprBase):
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self): return f"({self.lhs} / {self.rhs})"
@dataclass
class ModNode(ExprBase):
    lhs: ExprBase
    rhs: ExprBase

    def __str__(self): return f"({self.lhs} % {self.rhs})"

@dataclass
class NumberNode(ExprBase):
    value: int | float

    def __str__(self): return f"{self.value}"

@dataclass
class IdentNode(ExprBase):
    ident: str

@dataclass
class UnaryPlusNode(ExprBase):
    value: ExprBase

    def __str__(self): return f"+{self.value}"

@dataclass
class UnaryMinusNode(ExprBase):
    value: ExprBase

    def __str__(self): return f"-{self.value}"

@dataclass
class FactorialNode(ExprBase):
    value: ExprBase
    
    def __str__(self) -> str: return f"{self.value}!"

@dataclass
class FunctionCall(ExprBase):
    name: str
    args: list[ExprBase]

    def __str__(self): return f"{self.name}({', '.join(map(str, self.args))})"
