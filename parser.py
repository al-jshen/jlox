from error import ParseError
from expr import Binary, Expr, Grouping, Literal, Unary
from token_type import TokenType
from tokens import Token


class Parser:
    # grammar:

    # expression     → equality ;
    # equality       → comparison ( ( "!=" | "==" ) comparison )* ;
    # comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    # term           → factor ( ( "-" | "+" ) factor )* ;
    # factor         → unary ( ( "/" | "*" ) unary )* ;
    # unary          → ( "!" | "-" ) unary
    #                | primary ;
    # primary        → NUMBER | STRING | "true" | "false" | "nil"
    #                | "(" expression ")" ;

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def expression(self) -> Expr | ParseError:
        return self.equality()

    def equality(self) -> Expr | ParseError:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr | ParseError:
        expr = self.term()

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr | ParseError:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr | ParseError:
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr | ParseError:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr | ParseError:
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.TRUE):
            return Literal(True)

        if self.match(TokenType.FALSE):
            return Literal(False)

        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        return ParseError(self.peek(), "Expect expression.")

    def consume(self, type: TokenType, message: str) -> Token | ParseError:
        if self.check(type):
            return self.advance()

        raise ParseError(self.peek(), message)

    def match(self, *types: TokenType) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True

        return False

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False

        return self.peek().type == type

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                return

            self.advance()

    def parse(self):
        try:
            return self.expression()
        except ParseError as e:
            print(e)
            return None
