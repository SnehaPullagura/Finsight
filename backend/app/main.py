from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from backend.app.core.config import settings
from backend.app.core.exceptions import FinSightException
from backend.app.core.logging import logger
from backend.app.database.session import engine
from backend.app.database.base import Base
from backend.app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing FinSight Database Tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("FinSight API Service started successfully.")
    yield
    logger.info("Shutting down FinSight API Service...")
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="AI-Powered Financial Health, Cash-Flow Intelligence & Scenario Simulation Platform",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(FinSightException)
async def finsight_exception_handler(request: Request, exc: FinSightException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error_code": exc.error_code,
            "message": exc.detail,
            "extra": exc.extra
        },
        headers=exc.headers
    )

app.include_router(api_router)

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "platform": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT
    }

@app.get("/", tags=["System"])
async def root():
    return {
        "message": "Welcome to FinSight — AI-Powered Financial Health, Cash-Flow Intelligence & Scenario Simulation Platform",
        "docs": "/docs",
        "health": "/health"
    }
