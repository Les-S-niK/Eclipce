
## Built-in modules: ##
from typing import Coroutine

## Local modules: ##
from core.api_v1.sign_up.schemas import UserEncryptedRegistrationModel
from core.api_v1.token_auth import BcryptActions
from core.async_databases.async_sql import UserHook
from core.async_databases.async_sql.db_models import Users
from exceptions.user_exceptions import UserExistsException, UserRegistationException


class UserRegistrationService:
    """Service, that works with user registration."""
    def __init__(self, user_hook: UserHook):
        self.user_hook: UserHook = user_hook
    
    async def register_user(
        self,
        login: str,
        hashed_password: bytes
    ) -> Coroutine[None, None, None]:
        """Add the user to database and check the errors.

        Args:
            login (str): user login.
            hashed_password (bytes): user hashed by bcrypt password.

        
        """
        user: bool = await self.user_hook.append(
            login=login,
            hashed_password=hashed_password
        )
        self._check_register_valid(user=user)
    
    def _check_register_valid(self, user: bool | Users) -> None:
        """Validate database response.

        Args:
            user (bool | Users): database response to add command.

        Raises:
            UserExistsException: If user exists in database.
            UserRegistationException: If other database exseption.
        """
        if isinstance(user, Users):
            raise UserExistsException()
    
        if not user:
            raise UserRegistationException()


