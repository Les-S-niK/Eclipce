
## Built-in modules: ##
from typing import Optional, Coroutine
from base64 import b64decode
from asyncio import to_thread

## Third-party modules: ##
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from uuid import uuid4
from uuid import UUID

## Local modules: ##
from core.api_v1.keys.asym_keys.schemas import AsymmetricKeysPair
from core.async_databases.async_redis import asym_keys_redis


async def create_asymmetric_keys_dependency(key_lenght: Optional[int] = 2048) -> Coroutine[None, None, AsymmetricKeysPair]:
    """Create two asymmetric keys for data encryption.

    Args:
        key_lenght (int): key lenght in bits.

    Returns:
        AsymmetricKeysPair: private and public keys.
    """
    key: RsaKey = await to_thread(
        RSA.generate,
        key_lenght,
    )
    private_key: bytes = key.export_key()
    public_key: bytes = key.public_key().export_key()
    keys_id: UUID = uuid4()
    
    return AsymmetricKeysPair(
        keys_id=keys_id,
        private_key=private_key,
        public_key=public_key
    )


def decrypt_data_by_private_key(
    private_key: RsaKey,
    data_to_decode: bytes
) -> bytes:
    """Decrypt data by the private key.

    Args:
        private_key (str),
        data_to_decode (bytes).

    Returns:
        bytes: Decoded data.
    """
    data_to_decode: bytes = b64decode(data_to_decode)
    private_key: RsaKey = RSA.import_key(private_key)
    
    cipher: PKCS1_OAEP.PKCS1OAEP_Cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
    decoded_data: bytes = cipher.decrypt(data_to_decode)
    
    return decoded_data
