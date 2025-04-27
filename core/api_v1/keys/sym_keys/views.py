
## Built-in modules: ##
from asyncio import to_thread

## Third-party modules: ##
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from uuid import UUID

## Local modules: ##
from core.api_v1.keys.sym_keys.schemas import SymmetricKey, EncryptedSymmetricKey
from core.api_v1.keys.sym_keys.utils import save_symmetric_key_to_redis
from core.api_v1.keys.asym_keys import decrypt_data_by_private_key, get_asym_keys_from_redis
from core.api_v1.keys.asym_keys.schemas import AsymmetricKeysPair
from core.gnupg import gnupg_encrypt_key, GnupgFolderManager


symmetric_key_router: APIRouter = APIRouter(
    prefix="/api_v1/keys/sym_key",
    tags=["Symmetric Key"]
)

@symmetric_key_router.post(
    "/save/",
    description="Decrypt the symmetric key from the frontend key and save it."
)
async def save_symmetric_key(
    encrypted_symmetric_key: EncryptedSymmetricKey
) -> JSONResponse:
    """Decrypt the symmetric key from the frontend and save it.

    Args:
        encrypted_symmetric_key (EncryptedSymmetricKey): Ecrypted key model with uuid and key.

    Returns:
        SymmetricKey: symmetric key model.
    """
    asym_keys_uuid: UUID = encrypted_symmetric_key.asym_keys_id
    asym_keys_pair: AsymmetricKeysPair = await get_asym_keys_from_redis(asym_keys_uuid=asym_keys_uuid)
    
    decrypted_symmetric_key: bytes = await to_thread(
        decrypt_data_by_private_key,
        asym_keys_pair.private_key,
        encrypted_symmetric_key.sym_key,
    )
    symmetric_key: SymmetricKey = SymmetricKey(
        key_id=encrypted_symmetric_key.key_id,
        sym_key=decrypted_symmetric_key[:32],
        key_iv=decrypted_symmetric_key[32:48]
    )
    
    data_to_save = {
        "sym_key": symmetric_key.sym_key,
        "key_iv": symmetric_key.key_iv
    }
    await save_symmetric_key_to_redis(
        symmetric_key_id=symmetric_key.key_id,
        key_data_bytes=data_to_save
    )
    gnupg_symmetric_key: bytes = gnupg_encrypt_key(
        symmetric_key=symmetric_key
    )
    folder_manager: GnupgFolderManager = GnupgFolderManager(symmetric_key_id=symmetric_key.key_id)
    await folder_manager.write_key_in_file(encrypted_symmetric_key=gnupg_symmetric_key)
    
    return {"status": "ok"}



