from fastapi import FastAPI

from app.core.config import settings
from app.routers.health import router as health_router
from app.routers.todos import router as todos_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# Cấp 0 endpoints (/) và (/health) vẫn giữ ở root
app.include_router(health_router)

# API versioning
app.include_router(todos_router, prefix="/api/v1")