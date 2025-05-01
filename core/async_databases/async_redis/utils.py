
## Built-in modules: ##
from typing import Coroutine

## Third-party modules: ##
from uuid import UUID
from Crypto.PublicKey.RSA import RsaKey

## Local modules: ##
from core.api_v1.keys.asym_keys.schemas import AsymmetricKeysPair
from core.api_v1.keys.sym_keys.schemas import SymmetricKey
from core.async_databases.async_redis.db_engine import sym_key_redis, asym_keys_redis


async def get_asym_keys_from_redis(asym_keys_uuid: UUID) -> Coroutine[None, None, AsymmetricKeysPair]:
    """Get asym keys pair from the redis.

    Args:
        asym_keys_uuid (UUID): Asym keys UUID in the redis.

    Returns:
        Coroutine[None, None, AsymmetricKeysPair]. - Asymmetric keys pair object with id, public and private key.
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


async def get_symmetric_key_from_redis(key_id: str) -> Coroutine[None, None, SymmetricKey]:
    """Get the Symmetric key from Redis database.

    Args:
        key_id (str): symmetric key id.

    Returns:
        SymmetricKey: Key object with the key_id, sym_key and key_iv.
    """
    async with sym_key_redis.client() as connection:
        sym_key_hash = await connection.hgetall(key_id)
    
    sym_key = sym_key_hash.get(b'sym_key')
    key_iv = sym_key_hash.get(b'key_iv')
    
    return SymmetricKey(
        key_id=key_id,
        sym_key=sym_key,
        key_iv=key_iv,
    )