from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from tokens import Token


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


class ExprVisitor(ABC):
    def visit(self, expr: Expr):
        if isinstance(expr, Binary):
            return self.visit_binary(expr)
        if isinstance(expr, Grouping):
            return self.visit_grouping(expr)
        if isinstance(expr, Literal):
            return self.visit_literal(expr)
        if isinstance(expr, Unary):
            return self.visit_unary(expr)

    @abstractmethod
    def visit_binary(self, expr: Binary):
        pass

    @abstractmethod
    def visit_grouping(self, expr: Grouping):
        pass

    @abstractmethod
    def visit_literal(self, expr: Literal):
        pass

    @abstractmethod
    def visit_unary(self, expr: Unary):
        pass
