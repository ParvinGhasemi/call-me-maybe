# https://docs.python.org/3/library/json.html#basic-usage
# https://docs.python.org/3/library/json.html
# https://www.geeksforgeeks.org/python/python-json/

"""Loading project's JSON files."""


import json
from pathlib import Path
from typing import Any
# load vs loads in json
# __file__.resolve().parent

def load_json(path: Path) -> Any:
    try:
        with path.open("r") as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise ValueError(f"File not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {path}: {error.msg}"
            f"(line {error.lineno}, column {error.colno})"
        ) from error



def main() -> int:
    input_directory = (
        Path(__file__).resolve().parent / "data" / "input"
    )
    paths = [
        input_directory / "functions_definition.json",
        input_directory / "function_calling_tests.json",
    ]

    for path in paths:
        try:
            data = load_json(path)
        except ValueError as error:
            print(f"ERROR: {error}")
            return 1

        print(f"Loaded file: {path.name}")
        print(f"Python type: {type(data).__name__}")
        print()
        print(data)
        print("=" * 50)
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
