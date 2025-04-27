

## Built-in modules: ##
from typing import Optional

## Third-party modules: ##
from fastapi import Header

## Local modules: ##
from core.api_v1.token_auth.schemas import TokenModel, DecodedTokenModel, EncryptedTokenModel
from core.api_v1.token_auth import BcryptActions
from core.api_v1.token_auth.oauth2 import create_token
from core.api_v1.sign_up.schemas import UserRegistrationModel
from core.async_databases.async_sql import UserHook
from exceptions.token_exceptions import RefreshTokenValidationException
from config import REFRESH_TOKEN, ACCESS_TOKEN, ACCESS_TOKEN_EXPIRE_TIME, REFRESH_TOKEN_EXPIRE_TIME


def create_tokens_pair(data_to_endode) -> tuple[str]:
    """Create access and refresh tokens pair.

    Returns:
        tuple[TokenModel]: Two token models. (access_token, refresh_token)
    """
    jwt_access_token: str = create_token(
        data_to_encode=data_to_endode,
        token_type=ACCESS_TOKEN,
        expires_delta=ACCESS_TOKEN_EXPIRE_TIME,
    )
    jwt_refresh_token: str = create_token(
        data_to_encode=data_to_endode,
        token_type=REFRESH_TOKEN,
        expires_delta=REFRESH_TOKEN_EXPIRE_TIME
    )
    return (jwt_access_token, jwt_refresh_token)


async def get_user_from_payload(decoded_token: DecodedTokenModel) -> UserRegistrationModel:
    """Checks the decoded token payload.

    Args:
        decoded_token (DecodedTokenModel)

    Returns:
        UserRegistrationModel: The user registration model corresponding to the decoded token payload.
    """
    async_database_hook: UserHook = UserHook()
    user: UserRegistrationModel = await async_database_hook.get(
        one_object=True,
        login=decoded_token.login
    )
    
    return user


def check_refresh_token_valid(decoded_refresh_token: DecodedTokenModel) -> bool:
    """Checks the refresh token validity.

    Args:
        decoded_refresh_token (DecodedTokenModel)

    Raises:
        RefreshTokenValidationException: if token is't refresh token.

    Returns:
        bool: True if token is valid.
    """
    if not (decoded_refresh_token.token_type == REFRESH_TOKEN and decoded_refresh_token.login):
        raise RefreshTokenValidationException()
    
    return True


def hash_password(password: str) -> bytes:
    """Hash the password and return bytes. 

    Args:
        password (str): unhashed password.

    Returns:
        bytes: hashed password.
    """
    bcrypt: BcryptActions = BcryptActions(password=password)
    return bcrypt.hash_password()


def get_token_dependency(authorization: Optional[str] = Header(None))-> TokenModel:
    """Get OAuth2 token from the headers. 

    Args:
        headers (Annotated[str | None], Header): Given headers. Defaults to None.a

    Returns:
        Token: User access token 
        None: If token not in headers.
    """
    if authorization:
        token_data: list[str] = authorization.split(" ")
    else:
        return None
    
    return TokenModel(token=token_data[1])


def get_encrypted_token_dependency(authorization: Optional[str] = Header(None))-> TokenModel:
    """Get OAuth2 token from the headers. 

    Args:
        headers (Annotated[str | None], Header): Given headers. Defaults to None.a

    Returns:
        Token: User access token 
        None: If token not in headers.
    """
    if authorization:
        token_data: list = authorization.split(" ")
    else:
        return None
    
    return EncryptedTokenModel(encrypted_token=token_data[1])