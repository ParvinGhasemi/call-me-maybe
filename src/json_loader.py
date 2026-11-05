"""Load UTF-8 JSON files and report reading or parsing failures."""


import json
from pathlib import Path
from typing import Any


class InputLoadError(Exception):
    """Report a failure to read or parse an input file.

    The loader preserves the original exception in __cause__.
    """


def load_json(path: Path) -> Any:
    """Read and parse a UTF-8 JSON file.

    Args:
        path: Path to the input file.

    Returns:
        The decoded Python value, without schema validation.

    Raises:
        InputLoadError: If the file cannot be read, decoded as UTF-8, or
            parsed as JSON. The original exception is chained as the cause.

    The file is closed automatically, including when parsing fails.
    """
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
