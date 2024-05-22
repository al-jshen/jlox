import sys
from typing import Dict, List


def generate_imports(imports: Dict[str, str]):
    code: List[str] = []
    for lib, vals in imports.items():
        code.append(f"from {lib} import {vals}\n")
    return code


def generate_ast(
    base_name: str,
    types: Dict[str, str],
):
    code: List[str] = []

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

    return code


def generate_visitor(
    base_names: list[str],
    types: list[Dict[str, str]],
):
    assert len(base_names) == len(
        types
    ), "base_names and types must have the same length"

    code = []

    basename_lower = [bn.lower() for bn in base_names]

    # visitor interface
    code.append("class Visitor(ABC):\n")
    code.append(f"\tdef visit(self, val: {'|'.join(base_names)}):\n")

    for bnl, tps in zip(basename_lower, types):
        for class_name in tps.keys():
            code.append(f"\t\tif isinstance(val, {class_name}):\n")
            code.append(f"\t\t\treturn self.visit_{class_name.lower()}_{bnl}(val)\n")

    code.append("\n")

    for bnl, tps in zip(basename_lower, types):
        for class_name in tps.keys():
            code.append("\t@abstractmethod\n")
            code.append(
                f"\tdef visit_{class_name.lower()}_{bnl}(self, {bnl}: {class_name}):\n"
            )
            code.append("\t\tpass\n")

    return code


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast.py <output directory>")
        sys.exit(64)

    output_dir = sys.argv[1]

    outs = []

    # generate imports
    outs.extend(
        generate_imports(
            imports={
                "typing": "Any",
                "tokens": "Token",
                "abc": "ABC, abstractmethod",
                "dataclasses": "dataclass",
            },
        )
    )

    # generate expression classes and visitor
    expr_types = {
        "Binary": "left: Expr, operator: Token, right: Expr",
        "Grouping": "expression: Expr",
        "Literal": "value: Any",
        "Unary": "operator: Token, right: Expr",
    }
    outs.extend(generate_ast(base_name="Expr", types=expr_types))

    with open(f"{output_dir}/expr.py", "w") as f:
        f.writelines(outs)

    outs = []

    outs.extend(
        generate_imports(
            imports={
                "expr": "Expr",
                "abc": "ABC, abstractmethod",
                "dataclasses": "dataclass",
            },
        )
    )

    # generate statement classes and visitor
    stmt_types = {
        "Expression": "expression: Expr",
        "Print": "expression: Expr",
    }
    outs.extend(generate_ast(base_name="Stmt", types=stmt_types))

    with open(f"{output_dir}/stmt.py", "w") as f:
        f.writelines(outs)

    outs = []

    outs.extend(
        generate_imports(
            imports={
                "expr": "*",
                "stmt": "*",
                "abc": "ABC, abstractmethod",
            },
        )
    )
    outs.extend(
        generate_visitor(base_names=["Expr", "Stmt"], types=[expr_types, stmt_types])
    )

    with open(f"{output_dir}/visitor.py", "w") as f:
        f.writelines(outs)
