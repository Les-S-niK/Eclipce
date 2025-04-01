
## Built-in modules: ##
from typing import Optional, Coroutine, Any
from datetime import timedelta, timezone, datetime

## Third-party modules: ##
from aiobcrypt import hashpw, gensalt, checkpw
import jwt

## Local modules: ##
from config import SECRET_KEY, TOKEN_HASH_ALGORITHM
from core.async_database import Hook
from core.api_v1.sign_up.schemas import UserRegistrationModel
from core.async_database.db_models import Users

def create_access_token(
    data_to_encode: dict[str, Any],
    expires_delta: Optional[timedelta] = timedelta(minutes=15),
) -> str:
    """Create access token using given information.

    Args:
        data_to_encode (dict[str, Any]): dictionary with user data.
        expires_delta (Optional[timedelta], optional): Token expire time delta. Defaults to timedelta(minutes=15).

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


async def authenticate_user(user_login: str, user_password: str) -> Coroutine[Any, Any, bool | Users]:
    """Authenticate the user, check the password and user login. 

    Args:
        user_login (str)
        user_password (str)

    Returns:
        bool | User: False if user not in database. User model if user input is correctly.
    """
    async_database_hook: Hook = Hook(table="users")
    user: Users = await async_database_hook.get(
        _one_object=True,
        login=user_login,
    )
    if not user:
        return False
    
    bcrypt_actions: BcryptActions = BcryptActions(password=user_password)
    password_verify_result: bool = await bcrypt_actions.compare_password(hashed_password=user.hashed_pass)
    
    if not password_verify_result:
        return False
    
    return UserRegistrationModel(login=user.login, password=user.hashed_pass)


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