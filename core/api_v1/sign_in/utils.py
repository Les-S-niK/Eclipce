
## Built-in modules: ##
from typing import Optional

## Third-party modules: ##
from fastapi import Header

## Local modules: ##
from core.api_v1.token_auth.schemas import TokenModel

def get_token_dependency(authorization: Optional[str] = Header(None))-> TokenModel:
    """Get OAuth2 token from the headers. 

    Args:
        headers (Annotated[str | None], Header): Given headers. Defaults to None.a

    Returns:
        Token: User access token 
        None: If token not in headers.
    """
    if authorization:
        token_data: str = authorization.split(" ")
    else:
        return None
    
    return TokenModel(
        access_token=token_data[1],
        token_type=token_data[0]
    )