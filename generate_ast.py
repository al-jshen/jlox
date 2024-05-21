import sys
from typing import Dict, List


def generate_ast_and_visitor(
    output_dir: str,
    base_name: str,
    types: Dict[str, str],
    imports: Dict[str, str],
):
    code: List[str] = []

    for lib, vals in imports.items():
        code.append(f"from {lib} import {vals}\n")

    # expression classes

    code.append(f"\nclass {base_name}(ABC):\n")
    code.append("\tdef accept(self, visitor):\n")
    code.append("\t\treturn visitor.visit(self)\n\n")

    for class_name, fields in types.items():
        code.append("@dataclass\n")
        code.append(f"class {class_name}({base_name}):\n")
        for field in fields.split(", "):
            field_name, field_type = field.split(": ")
            code.append(f"\t{field_name}: {field_type}\n")
        code.append("\n")

    # visitor interface
    code.append(f"class {base_name}Visitor(ABC):\n")
    code.append("\tdef visit(self, expr: Expr):\n")
    for class_name in types.keys():
        code.append(f"\t\tif isinstance(expr, {class_name}):\n")
        code.append(f"\t\t\treturn self.visit_{class_name.lower()}(expr)\n")
    code.append("\n")

    for class_name in types.keys():
        code.append("\t@abstractmethod\n")
        code.append(f"\tdef visit_{class_name.lower()}(self, expr: {class_name}):\n")
        code.append("\t\tpass\n")

    with open(f"{output_dir}/{base_name.lower()}.py", "w") as f:
        f.writelines(code)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast.py <output directory>")
        sys.exit(64)

    output_dir = sys.argv[1]

    generate_ast_and_visitor(
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
            "abc": "ABC, abstractmethod",
            "dataclasses": "dataclass",
        },
    )
