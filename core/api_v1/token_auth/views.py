
## Local modules: ##
from typing import Any, Annotated

## Third-party modules: ##
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi import status

## Local modules: ##
from config import TOKEN_EXPIRE_TIME, TOKEN_TYPE
from core.api_v1.sign_up.schemas import UserRegistrationModel
from core.api_v1.token_auth.schemas import OAuth2PasswordUserForm, TokenModel
from core.api_v1.token_auth import create_access_token, authenticate_user


token_auth_router: APIRouter = APIRouter(
    prefix="/api_v1/token_auth",
    tags=["Token"]
)


@token_auth_router.post("/")
async def token_auth(user_registration_form: UserRegistrationModel) -> TokenModel:
    """Token auth enpoint to get token after user auth.

    Args:
        user_registration_form (Annotated[OAuth2PasswordUserForm, Depends): User form.

    Returns:
        TokenModel: OAuth2 jwt.
    """
    user_login: str = user_registration_form.login
    user_password: str = user_registration_form.password
    
    user_model: UserRegistrationModel = await authenticate_user(
        user_login=user_login,
        user_password=user_password
    )
    if not user_model:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user_data: dict[str, Any] = {
        "sub": user_login,
    }
    jwt_access_token: str = create_access_token(
        data_to_encode=user_data,
        expires_delta=TOKEN_EXPIRE_TIME,
    )
    
    return TokenModel(
        access_token=jwt_access_token,
        token_type=TOKEN_TYPE
    )