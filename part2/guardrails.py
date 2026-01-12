import ast


class GuardrailViolation(Exception):
    pass


class Guardrail:
    def __init__(self, code: str):
        self.tree = ast.parse(code)

    def validate(self):
        self._check_no_random()
        self._check_no_external_calls()

    def _check_no_random(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    if n.name == "random":
                        raise GuardrailViolation("Random module usage detected")

    def _check_no_external_calls(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    if n.name not in {"math", "statistics", "typing"}:
                        raise GuardrailViolation(f"External import detected: {n.name}")
