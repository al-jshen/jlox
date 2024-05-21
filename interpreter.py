from typing import Any

from expr import Binary, Expr, ExprVisitor, Grouping, Literal, Unary
from token_type import TokenType


class Interpreter(ExprVisitor):
    def visit_binary(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            return float(left) - float(right)
        elif expr.operator.type == TokenType.SLASH:
            return float(left) / float(right)
        elif expr.operator.type == TokenType.STAR:
            return float(left) * float(right)
        elif expr.operator.type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError("Operands must be two numbers or two strings.")
        elif expr.operator.type == TokenType.GREATER:
            return float(left) > float(right)
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            return float(left) >= float(right)
        elif expr.operator.type == TokenType.LESS:
            return float(left) < float(right)
        elif expr.operator.type == TokenType.LESS_EQUAL:
            return float(left) <= float(right)
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)

    def visit_grouping(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visit_literal(self, expr: Literal):
        return expr.value

    def visit_unary(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            return -float(right)
        elif expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)

        return None

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def is_truthy(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, float) or isinstance(value, int):
            return value != 0
        return True

    def is_equal(self, a: Any, b: Any) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b
