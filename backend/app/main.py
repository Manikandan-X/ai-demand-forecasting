from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import (
    InMemoryBackend
)

from app.db.base import Base
from app.db.session import engine

from app.models import *

from app.routers.auth import router as auth_router
from app.routers.user_management import (
    router as user_management_router
)
from app.routers.dataset import router as dataset_router
from app.routers.forecast import router as forecast_router
from app.routers.ai_insights import (
    router as ai_insights_router
)

from app.routers.forecast_intelligence import (
    router as forecast_intelligence_router
)

from app.routers.dashboard import router as dashboard_router
from app.routers.reports import router as reports_router
from app.routers.admin import router as admin_router
from app.routers.notification import router as notification_router
from app.routers.test import router as test_router
from app.routers.websocket import router as websocket_router

from app.core.exception_handler import global_exception_handler

from app.core.api_monitoring import (
    ApiMonitoringMiddleware
)

from slowapi.errors import (
    RateLimitExceeded
)

from slowapi.middleware import (
    SlowAPIMiddleware
)

from slowapi import _rate_limit_exceeded_handler

from app.core.rate_limiter import (
    limiter
)

from app.jobs.scheduler import (
    scheduler
)
from app.services.scheduler_service import (
    start_scheduler,
    stop_scheduler
)

from app.routers.automation import (
    router as automation_router
)

from app.routers import (
    automation_settings
)

from app.routers import (
    admin_automation
)

from app.routers.integrations import router as integrations_router
from app.routers.webhooks import router as webhooks_router
from app.routers.api_keys import router as api_keys_router

from app.routers.alert_settings import (
    router as alert_settings_router
)

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app):

    FastAPICache.init(
        InMemoryBackend()
    )

    start_scheduler()

    yield

    stop_scheduler()


app = FastAPI(
    title="AI Demand Forecasting API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_exception_handler(Exception, global_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000
)

app.add_middleware(
    SlowAPIMiddleware
)

app.add_middleware(
    ApiMonitoringMiddleware
)
# =====================
# ROUTES (CLEAN)
# =====================
app.include_router(auth_router)
app.include_router(dataset_router)
app.include_router(forecast_router)
app.include_router(user_management_router)
app.include_router(ai_insights_router)
app.include_router(forecast_intelligence_router)
app.include_router(dashboard_router)
app.include_router(reports_router)
app.include_router(admin_router)
app.include_router(notification_router)
app.include_router(test_router)
app.include_router(websocket_router)
app.include_router(automation_router)
app.include_router(automation_settings.router)
app.include_router(admin_automation.router)    
app.include_router(integrations_router)
app.include_router(webhooks_router)
app.include_router(api_keys_router)
app.include_router(alert_settings_router)

@app.get("/")
def root():
    return {"message": "API Running Successfully"}