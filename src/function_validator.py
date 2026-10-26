from typing import Literal
from pydantic import BaseModel, model_validator, Field, ConfigDict, ValidationError



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

# name
# description
# parameters
# return


class TypeDefinition(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    type: Literal["string", "number", "integer", "boolean"]

class FunctionDefinition(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    name: str
    description: str
    parameters: dict[str, TypeDefinition]
    returns: TypeDefinition
