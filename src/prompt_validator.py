from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError


class PromptEntry(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    prompt: str


def validate_prompts(data: Any) -> list[PromptEntry]:
    if not isinstance(data, list):
        raise ValueError("Prompts input must be a JSON array.")

    prompts: list[PromptEntry] = []
    for index, entry in enumerate(data):
        try:
            prompts.append(PromptEntry.model_validate(entry))
        except ValidationError as error:
            raise ValueError(
                f"Invalid value error at index {index}: {entry}"
            ) from error

    return prompts
