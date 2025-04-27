
## Built-in modules: ##
from typing import Annotated
from datetime import datetime

## Third-party modules: ##
from pydantic import BaseModel, Field, UUID4
from fastapi.security import OAuth2PasswordRequestForm


class KeyUUID(BaseModel):
    """Model for keys UUID"""
    key_id: Annotated[UUID4, Field(
        default=...,
        alias="key_id",
        title="UUID4 key id",
        description="Unique UUID4 for key/keys pair. "
    )]


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


class DecodedTokenModel(BaseModel):
    """Decoded token model."""
    login: Annotated[str, Field(
        default=...,
        alias="login",
        title="Unique user login",
        description="User login for decoded token.",
    )]
    expires_delta: Annotated[datetime, Field(
        default=...,
        alias="expires_delta",
        title="Token expiration date",
        description="Token expiration date for decoded token.",
    )]
    token_type: Annotated[str, Field(
        default=...,
        alias="token_type",
        title="Token type",
        description="Oauth2 token type",
    )]


class TokenModel(BaseModel):
    """Token model with necessary fields for auth."""
    token: Annotated[str, Field(
        default=...,
        alias="token",
        title="token",
        description="Access / Refresh token for user",
    )]


class EncryptedTokenModel(BaseModel):
    """Encrypted QAuth2 token model."""
    encrypted_token: Annotated[bytes, Field(
        default=...,
        alias="encrypted_token",
        title="Encrypted access token",
        description="Encrypted access / refresh token for user.",
    )]
