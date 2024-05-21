from typing import Any
from tokens import Token
from abc import ABC
from dataclasses import dataclass

class Expr(ABC):
	def accept(self, visitor):
		return visitor.visit(self)

class Binary(Expr):
	left: Expr
	operator: Token
	right: Expr

class Grouping(Expr):
	expression: Expr

class Literal(Expr):
	value: Any

class Unary(Expr):
	operator: Token
	right: Expr

