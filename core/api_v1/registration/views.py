
## Local modules: ##
from typing import Annotated

## Third-party modules: ##
from fastapi import APIRouter
from fastapi import Body
from fastapi.responses import JSONResponse

## Local modules: ##
from .models import UserRegistrationModel


registration_router: APIRouter = APIRouter(
    prefix="/api_v1/sign_up",
    tags=["Registration"]
)


@registration_router.post("/")
async def user_registration(user_registration_form: Annotated[UserRegistrationModel, Body()]) -> dict:
    ## TODO: send request to db and check user form. ##
    print(111)
    return {"message": "Okay"}