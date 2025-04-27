
## Third-party modules: ##
from fastapi import status
from fastapi.exceptions import HTTPException


class UserExistsException(HTTPException):
    """User exists in database exception.

    Args:
        HTTPException. 
    """
    def __init__(
        self,
        status_code=status.HTTP_409_CONFLICT,
        detail="User with this login already exists.",
        headers={"WWW-Authenticate": "Bearer"}
    ) -> None:
        super().__init__(status_code, detail, headers)


class UserRegistationException(HTTPException):
    """Unknown user registration exception.

    Args:
        HTTPException. 
    """
    def __init__(
        self,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to register the user.",
        headers={"WWW-Authenticate": "Bearer"}
    ) -> None:
        super().__init__(status_code, detail, headers)


class UserAuthException(HTTPException):
    """Can't authenticate the user exception.

    Args:
        HTTPException. 
    """
    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Can't authenticate the user. Check the login and password.",
        headers={"WWW-Authenticate": "Bearer"}
    ) -> None:
        super().__init__(status_code, detail, headers)
