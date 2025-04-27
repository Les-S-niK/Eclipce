
## Built-in modules: ##
from typing import Annotated

## Third-party modules: ##
from pydantic import BaseModel, Field
from uuid import UUID


class UserEncryptedRegistrationModel(BaseModel):
    """Encrypted by public key user form model."""
    key_id: Annotated[UUID, Field(
        default=...,
        alias="key_id",
        title="symmetric key id.",
        description="symmetric key id. It used to encrypt user data.",
    )]
    encrypted_login: Annotated[bytes, Field(
        default=...,
        alias="encrypted_login",
        title="Encrypted user login",
        description="Encrypted user login for registration",
    )]
    encrypted_password: Annotated[bytes, Field(
        default=...,
        alias="encrypted_password",
        title="UEncrypted user password",
        description="Encrypted user password for registration",
    )]


class UserRegistrationModel(BaseModel):
    """User registration form model."""
    login: Annotated[str, Field(
        default=...,
        alias="login",
        title="Unique user login",
        description="User login for registration",
        min_length=4,
        max_length=24,
    )]
    password: Annotated[str, Field(
        default=...,
        alias="password",
        title="User password",
        description="User password for registration",
        min_length=8,
    )]
