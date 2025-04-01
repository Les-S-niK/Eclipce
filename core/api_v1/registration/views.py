
## Local modules: ##
from typing import Annotated

## Third-party modules: ##
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status
from bcrypt import hashpw, gensalt

## Local modules: ##
from .models import UserRegistrationModel
from sql_hooks import Hook


registration_router: APIRouter = APIRouter(
    prefix="/api_v1/sign_up",
    tags=["Registration"]
)


@registration_router.post("/")
async def user_registration(user_registration_form: UserRegistrationModel) -> JSONResponse:
    """User registation endpoint in Registration router.

    Args:
        user_registration_form (UserRegistrationModel): User model from front-end form.

    Returns:
        JSONResponse: Json response to user.. 
    """
    user_login: str = user_registration_form.login
    user_password: str = user_registration_form.password
    hashed_user_password: bytes = hashpw(
        password=bytes(user_password.encode()),
        salt=gensalt(rounds=14),
    )
    
    async_sql_hook: Hook = Hook(table="users")
    database_response: bool = await async_sql_hook.append(
        login=user_login,
        hashed_password=hashed_user_password
    )
    if not database_response:
        return JSONResponse(
            content={
                "message": "Failed to register user",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
    return {
        "message": "User created successfully",
    }
    
    ## TODO: Add JWT tokens. Auto-generate headers for user. Bearer: Token. 