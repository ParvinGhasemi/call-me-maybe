from typing import Literal, Any
from pydantic import BaseModel, ConfigDict, ValidationError


"""
  {
    "name": "fn_add_numbers",
    "description": "Add two numbers together and return their sum.",
    "parameters": {
      "a": {
        "type": "number"
      },
      "b": {
        "type": "number"
      }
    },
    "returns": {
      "type": "number"
    }
  },
"""


class TypeDefinition(BaseModel):
    """Describe a parameter or return type."""
    model_config = ConfigDict(strict=True, extra="forbid")
    type: Literal["string", "number", "integer", "boolean"]


class FunctionDefinition(BaseModel):
    """Describe an available function and its argument types."""
    model_config = ConfigDict(strict=True, extra="forbid")

    name: str
    description: str
    parameters: dict[str, TypeDefinition]
    returns: TypeDefinition


def validate_functions(data: Any) -> list[FunctionDefinition]:
    """Validate a list of function definitions."""
    if not isinstance(data, list):
        raise TypeError(
            "Function definitions must be a JSON array."
        )

    functions: list[FunctionDefinition] = []
    names: set[str] = set()

    for index, entry in enumerate(data):
        try:
            function = FunctionDefinition.model_validate(entry)
        except ValidationError as error:
            raise ValueError(
                f"Invalid function definition at index {index}: {error}"
            ) from error
        if function.name in names:
            raise ValueError(f"Duplicate function name: {function.name}")
        names.add(function.name)
        functions.append(function)

    return functions
