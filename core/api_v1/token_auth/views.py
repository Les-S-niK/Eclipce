
## Local modules: ##
from typing import Annotated

## Third-party modules: ##
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

## Local modules: ##
from core.api_v1.token_auth.utils import (
    get_encrypted_token_dependency,
    check_refresh_token_valid
)
from core.api_v1.token_auth.oauth2 import decode_token, create_token
from core.api_v1.token_auth.schemas import TokenModel, DecodedTokenModel, EncryptedTokenModel
from core.api_v1.keys.sym_keys import AESDataDecrypter
from core.api_v1.keys.sym_keys.schemas import SymmetricKey
from core.api_v1.token_auth.schemas import KeyUUID
from core.gnupg import GnupgFolderManager, gnupg_decrypt_key
from core.async_databases.async_redis import get_symmetric_key_from_redis
from exceptions.token_exceptions import RefreshTokenValidationException
from config import ACCESS_TOKEN, ACCESS_TOKEN_EXPIRE_TIME


token_auth_router: APIRouter = APIRouter(
    prefix="/api_v1/token_auth",
    tags=["Token-auth"]
)

@token_auth_router.post(
    path="/refresh/",
    description="Endpoint to get access token by the refresh token."
)
async def refresh_access_token(
    symmetric_key_id: KeyUUID,
    encrypted_refresh_token: Annotated[EncryptedTokenModel, Depends(get_encrypted_token_dependency)]
) -> JSONResponse:
    """Checks the refresh token and return to user new access token.

    Args:
        refresh_token (Annotated[TokenModel, Depends)

    Returns:
        TokenModel: New access token.
    """
    key_id: str = str(symmetric_key_id.key_id)
    symmetric_key: SymmetricKey = await get_symmetric_key_from_redis(key_id=key_id)
    
    if symmetric_key.sym_key is None:
        folder_manager: GnupgFolderManager = GnupgFolderManager(symmetric_key_id=key_id)
        encrypted_symmetric_key: bytes = await folder_manager.get_key_from_file()
        symmetric_key: SymmetricKey = gnupg_decrypt_key(
            symmetric_key_id=key_id,
            encrypted_symmetric_key=encrypted_symmetric_key,
        )
    
    refresh_token: TokenModel = AESDataDecrypter(
        data_to_decrypt=encrypted_refresh_token.encrypted_token,
        symmetric_key=symmetric_key,
        decode_data_from_base64=True,
    ).decrypted_data
    
    if not refresh_token:
        raise RefreshTokenValidationException()
    
    refresh_token_model: TokenModel = TokenModel(token=refresh_token)
    decoded_refresh_token: DecodedTokenModel = decode_token(refresh_token_model)
    check_refresh_token_valid(decoded_refresh_token=decoded_refresh_token)
    
    data_to_encode: dict[str, str] = {
        "sub": decoded_refresh_token.login
    }
    access_token: str = create_token(
        data_to_encode=data_to_encode,
        token_type=ACCESS_TOKEN,
        expires_delta=ACCESS_TOKEN_EXPIRE_TIME
    )
    return {"access_token": access_token}
