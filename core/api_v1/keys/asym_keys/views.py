
## Built-in modules: ##
from typing import Annotated

## Third-party modules: ##
from fastapi import APIRouter, Depends

## Local modules: ##
from core.api_v1.keys.asym_keys.schemas import AsymmetricKeysPair
from core.api_v1.keys.asym_keys.utils import create_asymmetric_keys_dependency
from core.async_databases.async_redis import asym_keys_redis


asymmetric_keys_router: APIRouter = APIRouter(
    prefix="/api_v1/keys/asym_keys",
    tags=["Asymmetric Keys"],
)


@asymmetric_keys_router.get(
    path="/create/",
    description="Return a public asymmetric key from the keys pair. Private key is None.",
    response_model=AsymmetricKeysPair,
)
async def create_asymmetric_keys(
    keys_pair: Annotated[AsymmetricKeysPair, Depends(create_asymmetric_keys_dependency)]
) -> AsymmetricKeysPair:
    """Create asymmetric keys pair.

    Returns:
        JSONResponse.
    """
    data_to_save: dict = {
        "private_key": keys_pair.private_key,
        "public_key": keys_pair.public_key
    }
    async with asym_keys_redis.client() as connection:
        await connection.hset(str(keys_pair.keys_id), mapping=data_to_save)
        await connection.expire(str(keys_pair.keys_id), 60)
    
    return AsymmetricKeysPair(
        keys_id=keys_pair.keys_id,
        public_key=keys_pair.public_key,
        private_key=None
    )