import logging

from contextlib import asynccontextmanager

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, BackgroundTasks

from api.middleware.session import session_middleware
from api.packages.crud import create_packages_types
from api.packages.views import router as packages_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Start dependencies initialization.")
    await create_packages_types()
    yield


app = FastAPI(lifespan=lifespan, title="Package Delivery Microservice API")
app.include_router(packages_router)
app.add_middleware(BaseHTTPMiddleware, dispatch=session_middleware.dispatch)
