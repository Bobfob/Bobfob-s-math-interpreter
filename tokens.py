from dataclasses import dataclass
from typing import Any
from enum import Enum, auto

class TokenType(Enum):
    Identifier = auto()
    Assign = auto()
    NumberLit = auto()
    LParen = auto()
    RParen = auto()
    BinaryOp = auto()
    PostfixOp = auto()
    Comma = auto()

@dataclass
class Token:
    type: TokenType
    value: Any | None = None
