import sys
from typing import List, Dict


def generate_ast(
    output_dir: str,
    base_name: str,
    types: Dict[str, str],
    imports: Dict[str, str] = None,
    string_reps: bool = False,
):

    code: List[str] = []

    if imports:
        for lib, vals in imports.items():
            code.append(f"from {lib} import {vals}\n")

    code.append(f"class {base_name}:\n  pass\n\n")

    for class_name, fields in types.items():

        code.append(f"class {class_name}({base_name}):\n")
        code.append(f"  def __init__(self, {fields}):\n")
        for field in fields.split(", "):
            field_name, field_type = field.split(": ")
            code.append(f"    self.{field_name}: {field_type} = {field_name}\n")

        if string_reps:
            code.append(f"  def __str__(self):\n")
            str_rep = "".join(
                [" {self." + i.split(": ")[0] + "}" for i in fields.split(", ")]
            )
            code.append(f'    f"{str_rep.strip()}"\n')
        code.append("\n")

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
        {
            "Binary": "left: Expr, operator: Token, right: Expr",
            "Grouping": "expression: Expr",
            "Literal": "value: Any",
            "Unary": "operator: Token, right: Expr",
        },
        {"typing": "Any", "tokens": "Token"},
        string_reps=True,
    )
