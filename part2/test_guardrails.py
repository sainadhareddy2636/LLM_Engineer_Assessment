import pytest
from guardrails import Guardrail, GuardrailViolation


def test_random_detection():
    code = "import random"
    with pytest.raises(GuardrailViolation):
        Guardrail(code).validate()


def test_external_import_detection():
    code = "import requests"
    with pytest.raises(GuardrailViolation):
        Guardrail(code).validate()


def test_valid_code():
    code = "import math\nx = math.sqrt(4)"
    Guardrail(code).validate()
