from expr import *
from stmt import *
from abc import ABC, abstractmethod
class Visitor(ABC):
	def visit(self, val: Expr|Stmt):
		if isinstance(val, Binary):
			return self.visit_binary_expr(val)
		if isinstance(val, Grouping):
			return self.visit_grouping_expr(val)
		if isinstance(val, Literal):
			return self.visit_literal_expr(val)
		if isinstance(val, Unary):
			return self.visit_unary_expr(val)
		if isinstance(val, Expression):
			return self.visit_expression_stmt(val)
		if isinstance(val, Print):
			return self.visit_print_stmt(val)

	@abstractmethod
	def visit_binary_expr(self, expr: Binary):
		pass
	@abstractmethod
	def visit_grouping_expr(self, expr: Grouping):
		pass
	@abstractmethod
	def visit_literal_expr(self, expr: Literal):
		pass
	@abstractmethod
	def visit_unary_expr(self, expr: Unary):
		pass
	@abstractmethod
	def visit_expression_stmt(self, stmt: Expression):
		pass
	@abstractmethod
	def visit_print_stmt(self, stmt: Print):
		pass
