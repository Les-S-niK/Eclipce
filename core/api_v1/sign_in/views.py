
## Local modules: ##
from typing import Annotated, Optional, Any

## Third-party modules: ##
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi import status
from aiohttp import ClientSession
from jwt.exceptions import InvalidTokenError

## Local modules: ##
from core.api_v1.sign_in.utils import get_token_dependency
from core.api_v1.sign_up.schemas import UserRegistrationModel
from core.api_v1.token_auth.schemas import TokenModel
from core.api_v1.token_auth.oauth2 import authenticate_user, decode_access_token
from core.async_database import UserHook
from config import TOKEN_TYPE, TOKEN_AUTH_ENDP


authorization_router: APIRouter = APIRouter(
    prefix="/api_v1/sign_in",
    tags=["Authorization"]
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
    payload_exception: Exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user data.",
        headers={"WWW-Authenticate": TOKEN_TYPE}
    )
    if auth_token:
        try:
            user_login: str = decode_access_token(encoded_token=auth_token).login
        except InvalidTokenError:
            raise payload_exception
        
        async_database_hook: UserHook = UserHook()
        user: UserRegistrationModel = await async_database_hook.get(
            to_obj=True,
            login=user_login
        )
        if user:
            return auth_token

    if not user_registration_form:
        raise payload_exception
    
    user_login: str = user_registration_form.login
    user_password: str = user_registration_form.password
    user: UserRegistrationModel = await authenticate_user(
        user_login=user_login,
        user_password=user_password
    )
    if not user:
        raise payload_exception
    
    json_user_data: dict[str, str] = {
        "login": user.login,
        "password": user.password,
    }
    async with ClientSession() as session:
        async with session.post(
            url=TOKEN_AUTH_ENDP,
            json=json_user_data,
        ) as response: 
            json_response: dict[str, Any] = await response.json()
            access_token: TokenModel = TokenModel(**json_response)
    
    return access_token