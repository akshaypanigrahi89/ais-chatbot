from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from backend.config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    from backend.models.database import init_db
    init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_TAGLINE,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


def include_routers():
    from backend.api.auth_routes import router as auth_router
    from backend.api.chat_routes import router as chat_router
    from backend.api.admin_routes import router as admin_router

    app.include_router(auth_router)
    app.include_router(chat_router)
    app.include_router(admin_router)


include_routers()
