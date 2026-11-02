"""Testing Function definition validation"""

import unittest
from pathlib import Path
from copy import deepcopy

from src.function_validator import validate_functions
from src.json_loader import load_json


class TestFunctionValidator(unittest.TestCase):
    """Check valid Definition and reject invalid definitions"""

    def setUp(self) -> None:
        """Create a fresh valid definition before each test."""
        self.definition = {
            "name": "fn_add_numbers",
            "description": "Add two numbers.",
            "parameters": {
                "a": {"type": "number"},
                "b": {"type": "number"},
            },
            "returns": {"type": "number"},
        }

    def test_invalid_definition(self) -> None:
        """A valid definition produces a usable model."""
        functions = validate_functions([self.definition])
        self.assertEqual(len(functions), 1)
        self.assertEqual(functions[0].name, "fn_add_numbers")
        self.assertEqual(functions[0].parameters["a"].type, "number")

    def test_wrong_outer_types(self) -> None:
        """Input must be a list."""
        with self.assertRaises(TypeError):
            validate_functions(self.definition)

    def test_missing_field(self) -> None:
        """Every declared field is required"""
        for field in ("name", "description", "parameters", "returns"):
            with self.subTest(missing_field=field):
                definition = deepcopy(self.definition)
                del definition[field]

                with self.assertRaises(ValueError):
                    validate_functions([definition])

    def test_invalid_definitions(self) -> None:
        """Reject wrong types, extra fields, and invalid nested schemas."""
        changes = [
            {"name": 42},
            {"description": False},
            {"parameters": []},
            {"parameters": {"a": {"type": "banana"}}},
            {"parameters": {"a": {}}},
            {"parameters": {"a": {"type": "number", "other": 1}}},
            {"returns": {"type": "banana"}},
            {"other": "unexpected"},
        ]

        for change in changes:
            with self.subTest(change=change):
                definition = deepcopy(self.definition)
                definition.update(change)
                with self.assertRaises(ValueError):
                    validate_functions([definition])

    def test_duplicate_names(self) -> None:
        """Two definitions cannot share a function name."""
        with self.assertRaisesRegex(ValueError, "Duplicate function name"):
            validate_functions([self.definition, deepcopy(self.definition)])

    def test_distinct_names(self) -> None:
        """Different names are accepted and input order is preserved."""
        second = deepcopy(self.definition)
        second["name"] = "fn_another_add"
        functions = validate_functions([self.definition, second])
        self.assertEqual(
            [function.name for function in functions],
            ["fn_add_numbers", "fn_another_add"]
        )

    def test_supplied_definitions(self) -> None:
        """The supplied function definitions pass validation."""
        path = (
            Path(__file__).resolve().parent.parent
            / "src" / "data" / "input" / "functions_definition.json"
        )
        data = load_json(path)
        functions = validate_functions(data)
        self.assertGreater(len(functions), 0)
        self.assertEqual(len(functions), len(data))
