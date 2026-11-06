"""Validate loaded prompt data using strict Pydantic models."""

from importlib.metadata import entry_points
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError


class PromptEntry(BaseModel):
    """Represent a natural-language request without extra fields.

    Attributes:
        prompt: Request text. Empty strings are accepted.
    """
    model_config = ConfigDict(strict=True, extra="forbid")
    prompt: str


def validate_prompts(data: Any) -> list[PromptEntry]:
    """Validate loaded data and construct prompt models.

    Args:
        data: Unvalidated Python value returned by a JSON loader.

    Returns:
        Validated prompt entries in input order. An empty list is accepted.

    Raises:
        ValueError: If data is not a list or an entry fails validation.
            Entry failures preserve the Pydantic error as their cause.
    """
    if not isinstance(data, list):
        raise ValueError("Prompts input must be a JSON array.")

    prompts: list[PromptEntry] = []
    for index, entry in enumerate(data):
        try:
            prompts.append(PromptEntry.model_validate(entry))
        except ValidationError as error:
            messages: list[str] = []

            for issue in error.errors():
                location: str = ".".join(str(part) for part in issue['loc'])
                message: str = f"{location}: {issue['msg']}"
                messages.append(message)
            details: str = ";   ".join(messages)
            raise ValueError(
                f"Invalid value error at index {index}: {details}"
            ) from error

    return prompts
