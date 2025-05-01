
## Built-in modules: ##
from typing import Optional, Coroutine, Any
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
from exceptions.user_exceptions import UserAuthException


class AuthenticationService:
    """Service to authenticate user data."""
    def __init__(
        self,
        user_login: str,
        user_password: str,
    ) -> None:
        """Verify user data, compare inputed password with password in the database.
        UserRegistrationModel creating.

        Args:
            user_login (str): decrypted user login
            user_password (str): decrypted user password

        Raises:
            PayloadException: If password verification result if false.
        """
        self.user_login: str = user_login
        self.user_password: str = user_password
    
    async def create_registration_model(self) -> Coroutine[None, None, UserRegistrationModel]:
        await self._verify_user_password()
        self.user_registration_model: UserRegistrationModel = UserRegistrationModel(
            login=self.user_login,
            password=self.user_password
        )

    async def _get_user_from_db(self) -> Coroutine[None, None, Users]:
        """Get user model from the database.

        Returns:
            Users | False: User model if user in the database.
        Raises:
            UserAuthException if user is not.
        """
        async_database_hook: UserHook = UserHook()
        user: Users = await async_database_hook.get(
            one_object=True,
            login=self.user_login,
        )
        if not user:
            raise UserAuthException()
        
        return user

    async def _verify_user_password(self) -> Coroutine[None, None, bool]:
        """Verify and compare inputed by user password with password in the database.

        Returns:
            bool: True if password is valid, else: False.
        """
        user: Users = await self._get_user_from_db()
        bcrypt_actions: BcryptActions = BcryptActions(password=self.user_password)
        password_verify_result: bool = bcrypt_actions.compare_password(hashed_password=user.hashed_password)
        if not password_verify_result:
            raise PayloadException()
        
        return password_verify_result


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