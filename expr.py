from typing import Any
from tokens import Token
class Expr:
  pass

class Binary(Expr):
  def __init__(self, left: Expr, operator: Token, right: Expr):
    self.left: Expr = left
    self.operator: Token = operator
    self.right: Expr = right
  def __str__(self):
    f"{self.left} {self.operator} {self.right}"

class Grouping(Expr):
  def __init__(self, expression: Expr):
    self.expression: Expr = expression
  def __str__(self):
    f"{self.expression}"

class Literal(Expr):
  def __init__(self, value: Any):
    self.value: Any = value
  def __str__(self):
    f"{self.value}"

class Unary(Expr):
  def __init__(self, operator: Token, right: Expr):
    self.operator: Token = operator
    self.right: Expr = right
  def __str__(self):
    f"{self.operator} {self.right}"

