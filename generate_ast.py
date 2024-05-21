import sys
from typing import Dict, List


def generate_ast(
    output_dir: str,
    base_name: str,
    types: Dict[str, str],
    imports: Dict[str, str],
):
    code: List[str] = []

    for lib, vals in imports.items():
        code.append(f"from {lib} import {vals}\n")

    code.append(f"\nclass {base_name}(ABC):\n  pass\n\n")

    for class_name, fields in types.items():
        code.append(f"class {class_name}({base_name}):\n")
        for field in fields.split(", "):
            field_name, field_type = field.split(": ")
            code.append(f"\t{field_name}: {field_type}\n")
        code.append("\n")

    with open(f"{output_dir}/{base_name.lower()}.py", "w") as f:
        f.writelines(code)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast.py <output directory>")
        sys.exit(64)

    output_dir = sys.argv[1]

    generate_ast(
        output_dir=output_dir,
        base_name="Expr",
        types={
            "Binary": "left: Expr, operator: Token, right: Expr",
            "Grouping": "expression: Expr",
            "Literal": "value: Any",
            "Unary": "operator: Token, right: Expr",
        },
        imports={
            "typing": "Any",
            "tokens": "Token",
            "abc": "ABC",
            "dataclasses": "dataclass",
        },
    )
