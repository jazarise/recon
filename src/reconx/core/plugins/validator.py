import ast
from pathlib import Path
from reconx.core.plugins.exceptions import PluginValidationError


class SecurityScanner(ast.NodeVisitor):
    def __init__(self):
        self.unsafe_calls = []
        self.flagged_calls = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in ["eval", "exec"]:
                self.unsafe_calls.append(node.func.id)
        if isinstance(node.func, ast.Attribute):
            if (
                node.func.attr == "loads"
                and getattr(node.func.value, "id", "") == "pickle"
            ):
                self.unsafe_calls.append("pickle.loads")
            if (
                node.func.attr == "run"
                and getattr(node.func.value, "id", "") == "subprocess"
            ):
                for kw in node.keywords:
                    if kw.arg == "shell" and getattr(kw.value, "value", False) is True:
                        self.flagged_calls.append("subprocess.run(shell=True)")
        self.generic_visit(node)


def validate_plugin_security(file_path: Path):
    with open(file_path, "r", encoding="utf-8-sig") as f:
        code = f.read()

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise PluginValidationError(f"Syntax error in {file_path}: {e}")

    scanner = SecurityScanner()
    scanner.visit(tree)

    if scanner.unsafe_calls:
        raise PluginValidationError(
            f"Unsafe code detected in {file_path}: {scanner.unsafe_calls}"
        )

    if scanner.flagged_calls:
        # In a real app we might log this, for now we let it pass but it's flagged by our scanner
        pass


def validate_metadata(metadata: dict):
    required = ["name", "version", "author"]
    for req in required:
        if req not in metadata:
            raise PluginValidationError(f"Missing required metadata field: {req}")
