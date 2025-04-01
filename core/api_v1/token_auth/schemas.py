
## Built-in modules: ##
from typing import Annotated

## Third-party modules: ##
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordRequestForm

class OAuth2PasswordUserForm(OAuth2PasswordRequestForm):
    """Custom form model for OAuth2"""
    login: Annotated[str, Field(
        default=...,
        alias="login",
        title="Unique user login",
        description="User login for OAuth2 form.",
        min_length=4,
        max_length=24,
    )]


class TokenModel(BaseModel):
    """Token model with necessary fields for auth."""
    access_token: Annotated[str, Field(
        default=...,
        alias="access_token",
        title="Access token",
        description="Access token for user",
    )]
    token_type: Annotated[str, Field(
        default=...,
        alias="token_type",
        title="Token type",
        description="Oauth2 token type",
    )]
