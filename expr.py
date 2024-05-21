from typing import Any
from tokens import Token
from abc import ABC
from dataclasses import dataclass

class Expr(ABC):
	def accept(self, visitor):
		return visitor.visit(self)

@dataclass
class Binary(Expr):
	left: Expr
	operator: Token
	right: Expr

@dataclass
class Grouping(Expr):
	expression: Expr

@dataclass
class Literal(Expr):
	value: Any

@dataclass
class Unary(Expr):
	operator: Token
	right: Expr

