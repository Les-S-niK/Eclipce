
## Built-in modules: ##
from typing import Annotated
from typing import Optional
from asyncio import to_thread

## Third-party modules: ##
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

## Local modules: ##
from core.api_v1.sign_up.utils import UserRegistrationService
from core.api_v1.sign_up.schemas import UserEncryptedRegistrationModel, UserRegistrationModel
from core.api_v1.keys.sym_keys import AESDataEncrypter
from core.api_v1.keys.sym_keys import decrypt_user_data_by_sym_key
from core.api_v1.keys.sym_keys.schemas import SymmetricKey
from core.api_v1.token_auth import decode_token
from core.api_v1.token_auth import (
    get_token_dependency,
    get_user_from_payload,
    hash_password,
    create_tokens_pair
)
from core.api_v1.token_auth.schemas import TokenModel, DecodedTokenModel
from core.async_databases.async_sql import UserHook
from core.async_databases.async_redis import get_symmetric_key_from_redis
from config import ACCESS_TOKEN


registration_router: APIRouter = APIRouter(
    prefix="/api_v1/sign_up",
    tags=["Sign-up"]
)


@registration_router.post("/")
async def user_registration(
    auth_token: Annotated[TokenModel, Depends(get_token_dependency)],
    user_registration_form: Optional[UserEncryptedRegistrationModel],
) -> JSONResponse:
    """User registation endpoint in Registration router.

    Args:
        user_registration_form (UserRegistrationModel): User model from front-end form.

    Returns:
        JSONResponse: Json response to user. 
    """
    if auth_token:
        decoded_token: DecodedTokenModel = decode_token(encoded_token=auth_token)
        
        user: UserRegistrationModel = await get_user_from_payload(decoded_token=decoded_token)
        if user and decoded_token.token_type == ACCESS_TOKEN:
            return auth_token
    
    symmetric_key: SymmetricKey = await get_symmetric_key_from_redis(key_id=str(user_registration_form.key_id))
    
    user_login: bytes
    user_password: bytes
    user_login, user_password = await to_thread(
        decrypt_user_data_by_sym_key,
        user_registration_form,
        symmetric_key,
    )
    
    hashed_user_password: bytes = await to_thread(
        hash_password,
        user_password
    )
    
    async_db_hook: UserHook = UserHook()
    await UserRegistrationService(user_hook=async_db_hook).register_user(
        login=str(user_login),
        hashed_password=hashed_user_password
    )
    
    json_user_data: dict[str, str] = {
        "sub": user_login.decode()
    }

    tokens_pair: list[str] = list(create_tokens_pair(data_to_endode=json_user_data))
    encrypted_token: bytes = AESDataEncrypter(
        data_to_encrypt=tokens_pair[1],
        symmetric_key=symmetric_key,
        encode_data_to_base64=True
    ).encrypted_data
    tokens_pair[1] = encrypted_token
    
    return {
        "access_token": tokens_pair[0],
        "refresh_token": tokens_pair[1],
    }