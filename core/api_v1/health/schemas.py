
## Built-in modules: ##
from typing import Annotated

## Third-party modules: ##
from pydantic import BaseModel, Field 

## Local modules: ##


class HealthModel(BaseModel):
    """Health model with necessary fields.

    Args:
        BaseModel.
    """
    status: Annotated[str, Field(
        default=...,
        alias="status",
        title="Server status",
        description="Server status text respone."
    )]

