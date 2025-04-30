
## Local modules: ##
from typing import Annotated, Optional
from asyncio import to_thread

## Third-party modules: ##
from fastapi import APIRouter, Depends

## Local modules: ##
from core.api_v1.token_auth import (
    get_token_dependency, get_user_from_payload,
    create_token, decode_token, AuthenticationService
)
from core.api_v1.token_auth.schemas import TokenModel, DecodedTokenModel
from core.async_databases.async_redis import get_symmetric_key_from_redis
from core.api_v1.keys.sym_keys.schemas import SymmetricKey
from core.api_v1.keys.sym_keys import decrypt_user_data_by_sym_key
from core.api_v1.sign_up.schemas import UserEncryptedRegistrationModel, UserRegistrationModel
from config import ACCESS_TOKEN


authorization_router: APIRouter = APIRouter(
    prefix="/api_v1/sign_in",
    tags=["Sign-in"]
)


@authorization_router.post("/")
async def user_authorization(
    auth_token: Annotated[TokenModel, Depends(get_token_dependency)],
    user_registration_form: Optional[UserEncryptedRegistrationModel],
) -> TokenModel:
    """User registation endpoint in Registration router.

    Args:
        user_registration_form (UserRegistrationModel): User model from front-end form.

    Returns:
        JSONResponse: Json response to user. 
    """
    if auth_token:
        decoded_token: DecodedTokenModel = decode_token(encoded_token=auth_token)
        
        user: UserEncryptedRegistrationModel = await get_user_from_payload(decoded_token=decoded_token)
        if user and decoded_token.token_type == ACCESS_TOKEN:
            return auth_token
    
    symmetric_key: SymmetricKey = await get_symmetric_key_from_redis(key_id=str(user_registration_form.key_id))
    
    user_login: bytes
    user_password: bytes
    user_login, user_password = decrypt_user_data_by_sym_key(
        user_data=user_registration_form,
        symmetric_key=symmetric_key
    )
    user: UserRegistrationModel = await AuthenticationService(
        user_login=user_login,
        user_password=user_password
    ).create_registration_model()
    
    json_user_data: dict[str, str] = {
        "sub": user_login,
    }
    access_token: str = await create_token(
        data_to_encode=json_user_data,
        token_type=ACCESS_TOKEN,
    )
    
    return TokenModel(access_token)