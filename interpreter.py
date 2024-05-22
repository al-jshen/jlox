from typing import Any

from environment import Environment
from error import LoxRuntimeError
from expr import Assign, Binary, Expr, Grouping, Literal, Unary, Variable
from stmt import Expression, Print, Stmt, Var
from token_type import TokenType
from tokens import Token
from visitor import Visitor


class Interpreter(Visitor):
    def __init__(self):
        self.environment = Environment()

    def visit_binary_expr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        elif expr.operator.type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            else:
                raise LoxRuntimeError(
                    expr.operator,
                    f"Operands to operation {expr.operator} must both be strings or floats, got {type(left)} and {type(right)}",
                )
        elif expr.operator.type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)

        else:
            raise LoxRuntimeError(expr.operator, f"Unknown operator {expr.operator}")

    def check_number_operands(self, operator: Token, *operands: Any):
        for i, operand in enumerate(operands):
            if not isinstance(operand, float):
                raise LoxRuntimeError(
                    operator,
                    f"All operands to operation f{operator} must be floats, got {type(operand)} at index {i}",
                )

    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_unary_expr(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operands(expr.operator, right)
            return -float(right)
        elif expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)

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

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as e:
            print(e)

    def execute(self, stmt: Stmt):
        return stmt.accept(self)

    def stringify(self, value: Any) -> str:
        if value is None:
            return "nil"

        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text

        return str(value)

    def visit_expression_stmt(self, stmt: Expression):
        self.evaluate(stmt.expression)

    def visit_print_stmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_var_stmt(self, stmt: Var):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

    def visit_variable_expr(self, expr: Variable):
        return self.environment.get(expr.name)

    def visit_assign_expr(self, expr: Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
