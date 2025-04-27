
## Built-in modules: ##
from typing import Optional, Awaitable, Any
from datetime import timedelta, timezone, datetime

## Third-party modules: ##
from bcrypt import hashpw, gensalt, checkpw
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

## Local modules: ##
from config import SECRET_KEY, TOKEN_HASH_ALGORITHM, ACCESS_TOKEN_EXPIRE_TIME
from core.async_databases.async_sql import UserHook
from core.api_v1.sign_up.schemas import UserRegistrationModel
from core.api_v1.token_auth.schemas import DecodedTokenModel, TokenModel
from core.async_databases.async_sql.db_models import Users
from exceptions.token_exceptions import PayloadException, TokenExpiredException


def create_token(
    data_to_encode: dict[str, Any],
    token_type: str,
    expires_delta: Optional[timedelta] = ACCESS_TOKEN_EXPIRE_TIME,
) -> str:
    """Create access token using given information.

    Args:
        data_to_encode (dict[str, Any]): dictionary with user data.
        token_type (str): access / refresh token
        expires_delta (Optional[timedelta], optional): Token expire time delta. Defaults to ACCESS_TOKEN_EXPIRE_TIME.

    Returns:
        str: Generated token.
    """
    to_encode: dict[str, Any] = data_to_encode.copy()
    expire_time: datetime = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"type": token_type})
    to_encode.update({"exp": expire_time})
    encoded_jwt: str = jwt.encode(
        payload=to_encode,
        key=SECRET_KEY,
        algorithm=TOKEN_HASH_ALGORITHM,
    )
    return encoded_jwt


def decode_token(
    encoded_token: TokenModel
) -> DecodedTokenModel:
    """Decode access JWT token.

    Args:
        token (str): encoded JWT token.

    Returns:
        DecodedTokenModel: Decoded token information.
    """
    try: 
        payload: dict = jwt.decode(
            jwt=encoded_token.token, 
            key=SECRET_KEY,
            algorithms=[TOKEN_HASH_ALGORITHM],
            options={
                "verify_exp": True,
            }
        )
    except InvalidTokenError:
        raise PayloadException()
    except ExpiredSignatureError:
        raise TokenExpiredException()
    
    user_login: str = payload.get("sub")
    token_type: str = payload.get("type")
    token_expiration: datetime = payload.get("exp")
    
    if not user_login:
        raise PayloadException(detail="Missing \"sub\" field in token.")
    
    return DecodedTokenModel(
        login=user_login,
        expires_delta=token_expiration,
        token_type=token_type
    )


async def authenticate_user(user_login: str, user_password: str) -> Awaitable[UserRegistrationModel | bool]:
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
    password_verify_result: bool = bcrypt_actions.compare_password(hashed_password=user.hashed_password)
    
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
        self.bytes_password: bytes = password
    
    def compare_password(self, hashed_password: str) -> bool:
        """Compare hashed password with given password."""
        return checkpw(self.bytes_password, hashed_password.encode())

    def hash_password(self, rounds: Optional[int] = 12) -> bytes:
        """Hash the password and return hashed password.

        Args:
            rounds (Optional[int]): num of rounds.

        Returns:
            bytes: hashed password.
        """
        salt: bytes = gensalt(rounds=rounds)
        return hashpw(
            password=self.bytes_password,
            salt=salt
        )