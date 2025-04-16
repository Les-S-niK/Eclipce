
## Built-in modules: ##
from typing import Annotated

## Third-party modules: ##
from pydantic import BaseModel, Field


class UserRegistrationModel(BaseModel):
    """User registration form model."""
    login: Annotated[str, Field(
        default=...,
        alias="login",
        title="Unique user login",
        description="User login for registration",
        min_length=4,
        max_length=16,
    )]
    password: Annotated[str, Field(
        default=...,
        alias="password",
        title="User password",
        description="User password for registration",
        min_length=8,
    )]
