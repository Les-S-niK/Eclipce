
## Built-in modules: ##
from typing import Optional, Coroutine, Any
from datetime import timedelta, timezone, datetime

## Third-party modules: ##
from aiobcrypt import hashpw, gensalt, checkpw
import jwt

## Local modules: ##
from config import SECRET_KEY, TOKEN_HASH_ALGORITHM, TOKEN_EXPIRE_TIME
from core.async_database import UserHook
from core.api_v1.sign_up.schemas import UserRegistrationModel
from core.api_v1.token_auth.schemas import TokenDecodedModel, TokenModel
from core.async_database.db_models import Users


def create_access_token(
    data_to_encode: dict[str, Any],
    expires_delta: Optional[timedelta] = TOKEN_EXPIRE_TIME,
) -> str:
    """Create access token using given information.

    Args:
        data_to_encode (dict[str, Any]): dictionary with user data.
        expires_delta (Optional[timedelta], optional): Token expire time delta. Defaults to TOKEN_EXPIRE_TIME.

    Returns:
        str: Generated token.
    """
    to_encode: dict[str, Any] = data_to_encode.copy()
    expire_time: datetime = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire_time})
    encoded_jwt: str = jwt.encode(
        payload=to_encode,
        key=SECRET_KEY,
        algorithm=TOKEN_HASH_ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(
    encoded_token: TokenModel
) -> TokenDecodedModel:
    """Decode access JWT token.

    Args:
        token (str): encoded JWT token.

    Returns:
        TokenDecodedModel: Decoded token information.
    """
    payload: dict = jwt.decode(
        jwt=encoded_token.access_token, 
        key=SECRET_KEY,
        algorithms=[TOKEN_HASH_ALGORITHM]
    )
    user_login: str = payload.get("sub")
    token_expiration: datetime = payload.get("exp")
    
    return TokenDecodedModel(
        login=user_login,
        expires_delta=token_expiration,
    )


async def authenticate_user(user_login: str, user_password: str) -> Coroutine[Any, Any, bool | Users]:
    """Authenticate the user, check the password and user login. 

    Args:
        user_login (str)
        user_password (str)

    Returns:
        bool | User: False if user not in database. User model if user input is correctly.
    """
    async_database_hook: UserHook = UserHook()
    user: Users = await async_database_hook.get(
        one_object=True,
        login=user_login,
    )
    if not user:
        return False
    
    bcrypt_actions: BcryptActions = BcryptActions(password=user_password)
    password_verify_result: bool = await bcrypt_actions.compare_password(hashed_password=user.hashed_password)
    
    if not password_verify_result:
        return False
    
    return UserRegistrationModel(login=user_login, password=user_password)


class BcryptActions(object):
    """Class with main bcrypt actions (Hash password and check hashed password)."""
    def __init__(self, password: str) -> None:
        """Encode to bytes the password. Initialize class with main bcrypt actions.

        Args:
            password (str): password to work with.
        """
        self.bytes_password: bytes = password.encode()
    
    async def compare_password(self, hashed_password: str) -> Coroutine[Any, Any, bool]:
        """Compare hashed password with given password."""
        return await checkpw(self.bytes_password, hashed_password.encode())

    async def hash_password(self, rounds: Optional[int] = 12) -> Coroutine[Any, Any, bytes]:
        """Hash the password and return hashed password.

        Args:
            rounds (Optional[int]): num of rounds.

        Returns:
            bytes: hashed password.
        """
        salt: bytes = await gensalt(rounds=rounds)
        return await hashpw(
            password=self.bytes_password,
            salt=salt
        )