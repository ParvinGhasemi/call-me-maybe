"""Validate function definitions and reject duplicate function names."""

from typing import Literal, Any
from pydantic import BaseModel, ConfigDict, ValidationError


class TypeDefinition(BaseModel):
    """Describe a supported scalar JSON type.

    Attributes:
        type: One of string, number, integer, or boolean. Describes the
            expected type rather than validating an actual argument value.
    """
    model_config = ConfigDict(strict=True, extra="forbid")
    type: Literal["string", "number", "integer", "boolean"]


class FunctionDefinition(BaseModel):
    """Describe an available function with strict field validation.

    Attributes:
        name: Function identifier.
        description: Explanation of the function's purpose.
        parameters: Parameter names mapped to validated type descriptions.
        returns: Validated description of the return type.
    """
    model_config = ConfigDict(strict=True, extra="forbid")

    name: str
    description: str
    parameters: dict[str, TypeDefinition]
    returns: TypeDefinition


def validate_functions(data: Any) -> list[FunctionDefinition]:
    """Validate function definitions and require unique names.

    Args:
        data: Unvalidated Python value returned by a JSON loader.

    Returns:
        Validated definitions in input order. An empty list is accepted.

    Raises:
        TypeError: If data is not a list.
        ValueError: If an entry fails validation or function names repeat.
            Entry failures preserve the Pydantic error as their cause.
    """
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
