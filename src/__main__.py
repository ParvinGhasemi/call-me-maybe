"""Load and validate function definitions and prompts from default paths."""


import argparse
from pathlib import Path

from .json_loader import InputLoadError, load_json
from .function_validator import FunctionDefinition, validate_functions
from .prompt_validator import PromptEntry, validate_prompts


def main() -> int:
    """Load both input files, validate their contents, and print counts.

    Returns:
        Zero if both inputs pass validation, or one if loading or
        validation fails. Expected errors are printed for the user.
    """
    input_directory: Path = Path(__file__).resolve().parent / "data" / "input"
    parser = argparse.ArgumentParser(
        description="Load and validate function definitions and prompts (json)"
    )
    parser.add_argument(
        "--functions_definition",
        type=Path,
        default=input_directory / "functions_definition.json",
        required=False,
        help="give it the path to the functions definition JSON file.",
        metavar="FUNCTIONS_FILE",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=input_directory / "function_calling_tests.json",
        required=False,
        help="give it tha path to the prompts JSON file.",
        metavar="               PROMPTS_FILE",
    )
    args = parser.parse_args()

    try:
        function_data = (
            load_json(args.functions_definition)
        )
        prompts_data = (
            load_json(args.input)
        )
        functions: list[FunctionDefinition] = validate_functions(function_data)
        prompts: list[PromptEntry] = validate_prompts(prompts_data)

    except (InputLoadError, ValueError, TypeError) as error:
        print(f"ERROR (something went wrong!) -> {error}")
        return 1

    print(f"Loaded {len(functions)} function definitions.")
    print(f"Loaded {len(prompts)} prompts.")
    print("All inputs validated successfully!")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
