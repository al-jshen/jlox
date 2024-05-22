from expr import Expr
from abc import ABC, abstractmethod
from dataclasses import dataclass

class Stmt(ABC):
	def accept(self, visitor):
		return visitor.visit(self)

@dataclass
class Expression(Stmt):
	expression: Expr

@dataclass
class Print(Stmt):
	expression: Expr

