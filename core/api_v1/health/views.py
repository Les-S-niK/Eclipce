
## Built-in modules: ##

## Third-party modules: ##
from fastapi import APIRouter
from fastapi.responses import JSONResponse

## Local modules: ##
from core.api_v1.health.schemas import HealthModel


health_router: APIRouter = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@health_router.get(
    "/",
    response_model=HealthModel,
    description="Endpoint to check status of the server.",
)
async def check_health() -> JSONResponse:
    """Endpoint to check the server.

    Returns:
        JSONResponse.
    """
    return HealthModel(status="ok")