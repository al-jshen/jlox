import sys
from scanner import Scanner

class Lox:
    def __init__(self):
        self.had_error: bool = False

    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for t in tokens:
            print(t)

    # read a file and use self.run to run it
    def run_file(self, path: str):
        with open(path, 'r') as f:
            self.run(f.read())
        if self.had_error:
            sys.exit(65) 

    def run_prompt(self):
        while True:
            line = input('> ')
            if line == 'exit':
                break
            self.run(line)
            self.had_error = False

    def report_error(self, line: int, where: str, message: str):
        print(f'[line {line}] Error {where}: {message}')
        self.had_error = True


if __name__ == "__main__":
    args = sys.argv[1:]
    lox = Lox()

    # if there are no command line arguments
    if len(args) == 0:
        # print an error message
        print("Usage: lox.py <script>")
        # exit the program
        sys.exit(64)
    # if there is a command line argument
    elif len(args) == 1:
        lox.run_file(args[0])
    else:
        lox.run_prompt()

