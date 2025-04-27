
## Built-in modules: ##
from typing import Optional, Awaitable
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


async def get_asym_keys_from_redis(asym_keys_uuid: UUID) -> Awaitable[AsymmetricKeysPair]:
    """Get asym keys pair from the redis.

    Args:
        asym_keys_uuid (UUID): Asym keys UUID in the redis.

    Returns:
        Awaitable[AsymmetricKeysPair]. - Asymmetric keys pair object with id, public and private key.
    """
    async with asym_keys_redis.client() as connection:
        asym_keys: dict[str, bytes] = await connection.hgetall(str(asym_keys_uuid))
    private_key: RsaKey = asym_keys.get(b"private_key")
    public_key: bytes = asym_keys.get(b"public_key")
    
    return AsymmetricKeysPair(
        keys_id=asym_keys_uuid,
        public_key=public_key,
        private_key=private_key,
    )


async def create_asymmetric_keys_dependency(key_lenght: Optional[int] = 2048) -> Awaitable[AsymmetricKeysPair]:
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
