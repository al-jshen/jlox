from expr import Binary, Expr, ExprVisitor, Grouping, Literal, Unary
from token_type import TokenType
from tokens import Token


class AstPrinter(ExprVisitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def visit_binary(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visit_literal(self, expr: Literal):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr):
        return f"({name} {' '.join([expr.accept(self) for expr in exprs])})"


if __name__ == "__main__":
    from expr import Binary, Unary, Literal, Grouping

    expr = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )

    printer = AstPrinter()
    print(printer.print(expr))
