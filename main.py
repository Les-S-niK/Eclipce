
## Built-in modules: ## 

## Third-party modules: ##
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv  
from uvicorn import run

## Local modules: ##
from config import APP_VERSION, SERVER_HOST, SERVER_PORT, CORSMiddleWareSettings
from core.api_v1.sign_up import registration_router
from core.api_v1.token_auth import token_auth_router
from core.api_v1.sign_in import authorization_router
from core.api_v1.keys.asym_keys import asymmetric_keys_router
from core.api_v1.keys.sym_keys import symmetric_key_router
from core.api_v1.health import health_router


load_dotenv(override=True, verbose=True)

all_routers: list[APIRouter] = [
    registration_router,
    token_auth_router,
    authorization_router,
    asymmetric_keys_router,
    symmetric_key_router,
    health_router
]

app: FastAPI = FastAPI(
    version=APP_VERSION,
    debug=True,
)

for router in all_routers:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=CORSMiddleWareSettings.ALLOWED_ORIGINS,
    allow_credentials=CORSMiddleWareSettings.ALLOWED_CREDENTIALS,
    allow_methods=CORSMiddleWareSettings.ALLOWED_METHODS,
    allow_headers=CORSMiddleWareSettings.ALLOWED_HEADERS,
)


if __name__ == "__main__":
    run(
        "main:app",
        reload=True,
        host=SERVER_HOST,
        port=SERVER_PORT
    )