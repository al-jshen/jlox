import sys

from interpreter import Interpreter
from parser import Parser
import scanner


class Lox:
    def __init__(self):
        self.interpreter = Interpreter()
        self.had_error: bool = False

    def run(self, source: str):
        _scanner = scanner.Scanner(source, self)
        tokens = _scanner.scan_tokens()
        parser = Parser(tokens)
        statements = parser.parse()
        self.interpreter.interpret(statements)

    # read a file and use self.run to run it
    def run_file(self, path: str):
        with open(path, "r") as f:
            self.run(f.read())
        if self.had_error:
            sys.exit(65)

    def run_prompt(self):
        while True:
            line = input("> ")
            if line == "exit":
                break
            self.run(line)
            self.had_error = False


if __name__ == "__main__":
    args = sys.argv[1:]
    lox = Lox()

    # if there are no command line arguments
    if len(args) > 1:
        # print an error message
        print("Usage: lox.py <script>")
        # exit the program
        sys.exit(64)
    # if there is a command line argument
    elif len(args) == 1:
        lox.run_file(args[0])
    else:
        lox.run_prompt()
