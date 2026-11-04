"""Try loading and validating the supplied function definitions."""

from pathlib import Path

from .function_validator import validate_functions
from .json_loader import InputLoadError, load_json


def main() -> int:
    """Load function definitions and report validation errors."""
    path = (
        Path(__file__).resolve().parent
        / "data"
        / "input"
        / "functions_definition.json"
    )

    try:
        data = load_json(path)
        functions = validate_functions(data)
    except (InputLoadError, TypeError, ValueError) as error:
        print(f"Error: {error}")
        return 1

    for function in functions:
        print(function.name)
        # print(function.parameters["a"].type)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
