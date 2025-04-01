
## Local modules: ##
from typing import Annotated, Optional

## Third-party modules: ##
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi import status
import jwt
from jwt.exceptions import InvalidTokenError

## Local modules: ##
from core.api_v1.sign_in.utils import get_token_dependency
from core.api_v1.sign_up.schemas import UserRegistrationModel
from core.api_v1.token_auth.schemas import TokenModel
from core.api_v1.token_auth.oauth2 import authenticate_user, create_access_token
from core.async_database import Hook
from config import SECRET_KEY, TOKEN_HASH_ALGORITHM, TOKEN_TYPE, TOKEN_EXPIRE_TIME


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
            payload: dict = jwt.decode(
                jwt=auth_token.access_token, 
                key=SECRET_KEY,
                algorithms=[TOKEN_HASH_ALGORITHM]
            )
            user_login: str = payload.get("sub")
        
        except InvalidTokenError:
            raise payload_exception
        
        async_database_hook: Hook = Hook(table="users")
        user: UserRegistrationModel = async_database_hook.get(
            to_obj=True,
            login=user_login
        )
        if user:
            return auth_token

    user_login: str = user_registration_form.login
    user_password: str = user_registration_form.password
    user: UserRegistrationModel = await authenticate_user(
        user_login=user_login,
        user_password=user_password
    )
    if not user:
        raise payload_exception
    
    access_token: str = create_access_token(
        data_to_encode={"sub": user_login},
        expires_delta=TOKEN_EXPIRE_TIME
    )
    
    return TokenModel(
        access_token=access_token,
        token_type=TOKEN_TYPE
    )