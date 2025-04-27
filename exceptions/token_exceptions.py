
## Third-party modules: ##
from fastapi import status
from fastapi.exceptions import HTTPException

## Local modules: ##
from config import BEARER


class PayloadException(HTTPException):
    """Token payload exception.

    Args:
        HTTPException. 
    """
    def __init__(
        self,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate user data.",
        headers = {"WWW-Authenticate": BEARER}
    ) -> None:
        super().__init__(status_code, detail, headers)
        


class TokenExpiredException(HTTPException):
    """Token payload exception.

    Args:
        HTTPException. 
    """
    def __init__(
        self,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Token expired.",
        headers = {"WWW-Authenticate": BEARER}
    ) -> None:
        super().__init__(status_code, detail, headers)


class RefreshTokenValidationException(HTTPException):
    """Refresh token validation exception.

    Args:
        HTTPException. 
    """
    def __init__(
        self,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token.",
        headers={"WWW-Authenticate": "Bearer"}
    ) -> None:
        super().__init__(status_code, detail, headers)

