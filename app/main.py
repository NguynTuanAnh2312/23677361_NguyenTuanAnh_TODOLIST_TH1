from fastapi import FastAPI

from app.core.config import settings
from app.routers.health import router as health_router
from app.routers.todos import router as todos_router
from app.routers.auth import router as auth_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(health_router)
app.include_router(todos_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")