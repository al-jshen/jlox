from abc import ABC

from token_type import TokenType
from tokens import Token


class LoxError(ABC):
    def make_error(self, line: int, where: str, message: str):
        return f"[line {line}] Error {where}: {message}"


class ParseError(LoxError, Exception):
    def __init__(self, token: Token, message: str):
        if token.type == TokenType.EOF:
            msg = self.make_error(token.line, "at end", message)
        else:
            msg = self.make_error(token.line, f"at '{token.lexeme}'", message)

        super(Exception).__init__(msg)


class LoxRuntimeError(LoxError, Exception):
    def __init__(self, token: Token, message: str):
        msg = self.make_error(token.line, "", message)
        super(Exception).__init__(msg)
