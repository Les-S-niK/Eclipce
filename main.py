
## Built-in modules: ##

## Third-party modules: ##
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

## Local modules: ##
from config import APP_VERSION, CORSMiddleWareSettings
from core.api_v1.registration import registration_router


app: FastAPI = FastAPI(
    version=APP_VERSION,
    debug=True,
)
app.include_router(registration_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORSMiddleWareSettings.ALLOWED_ORIGINS,
    allow_credentials=CORSMiddleWareSettings.ALLOWED_CREDENTIALS,
    allow_methods=CORSMiddleWareSettings.ALLOWED_METHODS,
    allow_headers=CORSMiddleWareSettings.ALLOWED_HEADERS,
)


if __name__ == "__main__":
    run("main:app", reload=False)