import sys
from typing import List


def generate_ast(output_dir: str, base_name: str, types: List[List[str]]):

    code: List[str] = []

    code.append("from typing import Any\n")
    code.append("from tokens import Token\n\n")

    code.append(f"class {base_name}:\n  pass\n\n")

    for t in types:
        class_name = t[0]
        fields = t[1]

        code.append(f"class {class_name}({base_name}):\n")
        code.append(f"  def __init__(self, {fields}):\n")
        for field in fields.split(", "):
            field_name, field_type = field.split(": ")
            code.append(f"    self.{field_name}: {field_type} = {field_name}\n\n")

    with open(f"{output_dir}/{base_name.lower()}.py", "w") as f:
        f.writelines(code)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast.py <output directory>")
        sys.exit(64)

    output_dir = sys.argv[1]

    generate_ast(
        output_dir,
        "Expr",
        [
            ["Binary", "left: Expr, operator: Token, right: Expr"],
            ["Grouping", "expression: Expr"],
            ["Literal", "value: Any"],
            ["Unary", "operator: Token, right: Expr"],
        ],
    )
