import ast


def analyze_code(code: str) -> list[dict]:
    issues = []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [{
            "line": e.lineno or 1,
            "severity": "error",
            "message": f"Syntax error: {e.msg}",
        }]

    for i, line in enumerate(code.splitlines(), start=1):
        if len(line) > 79:
            issues.append({"line": i, "severity": "style",
                           "message": "Line is longer than 79 characters"})
        if "TODO" in line:
            issues.append({"line": i, "severity": "info",
                           "message": "Unresolved TODO comment"})

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not ast.get_docstring(node):
            issues.append({"line": node.lineno, "severity": "style",
                           "message": f"Function '{node.name}' has no docstring"})
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append({"line": node.lineno, "severity": "warning",
                           "message": "Bare 'except:' hides errors; catch a specific exception"})
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "print"):
            issues.append({"line": node.lineno, "severity": "info",
                           "message": "print() found; consider using logging"})

    return sorted(issues, key=lambda x: x["line"])
