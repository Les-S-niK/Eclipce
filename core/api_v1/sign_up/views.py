
## Local modules: ##
from typing import Any

## Third-party modules: ##
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import status

## Local modules: ##
from config import TOKEN_EXPIRE_TIME
from core.api_v1.sign_up.schemas import UserRegistrationModel
from core.api_v1.token_auth.schemas import TokenModel
from core.api_v1.token_auth.oauth2 import BcryptActions
from core.api_v1.token_auth.oauth2 import create_access_token
from core.async_database import Hook



registration_router: APIRouter = APIRouter(
    prefix="/api_v1/sign_up",
    tags=["Registration"]
)


@registration_router.post("/")
async def user_registration(user_registration_form: UserRegistrationModel) -> TokenModel:
    """User registation endpoint in Registration router.

    Args:
        user_registration_form (UserRegistrationModel): User model from front-end form.

    Returns:
        JSONResponse: Json response to user. 
    """
    user_login: str = user_registration_form.login
    user_password: str = user_registration_form.password
    bcrypt_actions: BcryptActions = BcryptActions(password=user_password)
    hashed_user_password: bytes = await bcrypt_actions.hash_password()
    
    async_sql_hook: Hook = Hook(table="users")
    database_response: bool = await async_sql_hook.append(
        login=user_login,
        hashed_password=hashed_user_password
    )

    if not database_response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register the user.",
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
        token_type="Bearer"
    )