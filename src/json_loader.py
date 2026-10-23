# https://docs.python.org/3/library/json.html#basic-usage
# https://docs.python.org/3/library/json.html
# https://www.geeksforgeeks.org/python/python-json/

"""Loading project's JSON files."""


import json
from pathlib import Path
from typing import Any


class InputLoadError(Exception):
    """Raised when an input file cannot be read or parsed."""


def load_json(path: Path) -> Any:
    """Read JSON, raising InputLoadError if loading fails."""
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise InputLoadError(f"File not found: {path}") from error
    except json.JSONDecodeError as error:
        raise InputLoadError(
            f"Invalid JSON in {path}: {error.msg}"
            f"(line {error.lineno}, column {error.colno})"
        ) from error
    except UnicodeDecodeError as error:
        raise InputLoadError(f"File is not valid UTF-8: {path}") from error
    except OSError as error:
        raise InputLoadError(
            f"Could not read {path}: {error.strerror}"
        ) from error


def main() -> int:
    input_directory = (
        Path(__file__).resolve().parent / "data" / "input"
    )
    paths = [
        # input_directory / "functions_definition.json",
        input_directory / "function_calling_tests.json",
        input_directory,
        input_directory / "invalid_syntax.json"
    ]

    for path in paths:
        try:
            data = load_json(path)
        except InputLoadError as error:
            print(f"ERROR: {error}")
            print()
            print(error.__cause__)
            return 1

        print(f"Loaded file: {path.name}")
        print(f"Python type: {type(data).__name__}")
        print()
        print(data)
        print("=" * 50)
        print()

    return 0






# """ test main """
# from .prompt_validator import validate_prompts
# def main() -> int:
#     """Try every input fixture and report loading or validation failures."""
#     input_directory = (
#         Path(__file__).resolve().parent / "data" / "input"
#     )

#     paths = sorted(input_directory.glob("*.json"))
#     paths.extend([
#         input_directory / "missing.json",
#         input_directory,  # A directory instead of a file.
#     ])

#     failures = 0

#     for path in paths:
#         print()
#         print(f"\nTesting: {path.name}")

#         try:
#             data = load_json(path)
#         except InputLoadError as error:
#             failures += 1
#             print(f"LOAD ERROR: {error}")

#             cause = error.__cause__
#             if cause is not None:
#                 print(f"Original error: {type(cause).__name__}")

#             continue

#         print("Loading succeeded.")

#         if path.name == "functions_definition.json":
#             print("Skipping prompt validation: function definitions.")
#             continue

#         try:
#             prompts = validate_prompts(data)
#         except ValueError as error:
#             failures += 1
#             print(f"VALIDATION ERROR: {error}")

#             cause = error.__cause__
#             if cause is not None:
#                 print(cause)

#             continue

#         print(f"Validation succeeded: {len(prompts)} prompt(s).")

#     print(f"\nFinished: {failures} input(s) rejected.")
#     return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
