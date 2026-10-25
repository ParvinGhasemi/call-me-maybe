"""Test JSON loading and prompt validation."""


import json
import unittest
from pathlib import Path


from src.json_loader import InputLoadError, load_json
from src.prompt_validator import validate_prompts


INPUT_DIRECTORY = (
    Path(__file__).resolve().parent.parent / "src" / "data" / "input"
)


class TestJsonLoader(unittest.TestCase):
    """ Check Successful Loading and the causes of the failure. """

    def test_valid_json(self) -> None:
        """A valid file produces the expected python values."""
        data = load_json(INPUT_DIRECTORY / "valid.json")
        self.assertEqual(data, [{"prompt": "Greet Shrek"}])

    def test_loading_errors(self) -> None:
        """Each invalid input raises the expected underlying error."""
        cases = [
            ("invalid_syntax.json", json.JSONDecodeError),
            ("empty_file.json", json.JSONDecodeError),
            ("invalid_encoding.json", UnicodeDecodeError),
            ("missing.json", FileNotFoundError),
            ("invalid_permission.json", PermissionError),
        ]
        for filename, expected_cause in cases:
            with self.subTest(filename=filename):
                with self.assertRaises(InputLoadError) as caught_err:
                    load_json(INPUT_DIRECTORY / filename)
                self.assertIsInstance(
                    caught_err.exception.__cause__,
                    expected_cause
                )

    def test_directory_instead_of_file(self) -> None:
        """Opening the input directory as a file fails."""
        with self.assertRaises(InputLoadError) as caught:
            load_json(INPUT_DIRECTORY)

        self.assertIsInstance(caught.exception.__cause__, IsADirectoryError)


class TestPromptValidator(unittest.TestCase):
    """Check the structure of successfully loaded JSON."""

    def test_valid_prompt(self) -> None:
        """A valid prompt becomes an accessible model object."""
        data = load_json(INPUT_DIRECTORY / "valid.json")
        prompts = validate_prompts(data)

        self.assertEqual(len(prompts), 1)
        self.assertEqual(prompts[0].prompt, "Greet Shrek")

    def test_invalid_prompts(self) -> None:
        """Valid JSON with the wrong structure is rejected."""
        filenames = [
            "empty.json",
            "extra_field.json",
            "wrong_outer_type.json",
            "wrong_prompt_type.json",
        ]
        for filename in filenames:
            with self.subTest(filename=filename):
                data = load_json(INPUT_DIRECTORY / filename)
                with self.assertRaises(ValueError):
                    validate_prompts(data)

    def test_supplied_prompts(self) -> None:
        """The supplied prompts pass validation."""
        data = load_json(INPUT_DIRECTORY / "function_calling_tests.json")
        prompts = validate_prompts(data)

        self.assertEqual(len(prompts), len(data))
