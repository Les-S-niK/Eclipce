
## Local modules: ##
from typing import Annotated, Optional

## Third-party modules: ##
from fastapi import APIRouter, Depends

## Local modules: ##
from core.api_v1.token_auth.schemas import TokenModel
from core.api_v1.token_auth.oauth2 import authenticate_user, create_token
from core.api_v1.sign_up.schemas import UserRegistrationModel
from core.api_v1.token_auth import get_token_dependency, get_user_from_payload
from exceptions.token_exceptions import PayloadException
from config import BEARER


authorization_router: APIRouter = APIRouter(
    prefix="/api_v1/sign_in",
    tags=["Sign-in"]
)


@authorization_router.post("/")
async def user_authorization(
    auth_token: Annotated[TokenModel, Depends(get_token_dependency)],
    user_registration_form: Optional[UserRegistrationModel] = None,
) -> TokenModel:
    """User registation endpoint in Registration router.

    Args:
        user_registration_form (UserRegistrationModel): User model from front-end form.

    Returns:
        JSONResponse: Json response to user. 
    """
    if auth_token:
        user: UserRegistrationModel = await get_user_from_payload(auth_token=auth_token)
        if user:
            return auth_token

    if not user_registration_form:
        raise PayloadException()
    
    user_login: str = user_registration_form.login
    user_password: str = user_registration_form.password
    user: UserRegistrationModel = await authenticate_user(
        user_login=user_login,
        user_password=user_password
    )
    if not user:
        raise PayloadException()
    
    json_user_data: dict[str, str] = {
        "login": user_login,
    }
    access_token: str = await create_token(data_to_encode=json_user_data)
    
    return TokenModel(access_token)