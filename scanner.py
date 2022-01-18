from token import Token
from typing import List, Union

class Scanner:
    def __init__(self, source: str):
        self.source = source

    def scan_tokens(self) -> List[Token]:
        pass
