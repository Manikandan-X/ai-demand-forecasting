from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.db.base import Base
from app.db.session import engine

from app.models import *

from app.routers.auth import router as auth_router
from app.routers.dataset import router as dataset_router
from app.routers.forecast import router as forecast_router
from app.routers.dashboard import router as dashboard_router
from app.routers.reports import router as reports_router
from app.routers.admin import router as admin_router
from app.routers.notification import router as notification_router
from app.routers.test import router as test_router
from app.routers.websocket import router as websocket_router

from app.core.exception_handler import global_exception_handler

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Demand Forecasting API",
    docs_url="/docs",
    redoc_url="/redoc"
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

# =====================
# ROUTES (CLEAN)
# =====================
app.include_router(auth_router)
app.include_router(dataset_router)
app.include_router(forecast_router)
app.include_router(dashboard_router)
app.include_router(reports_router)
app.include_router(admin_router)
app.include_router(notification_router)
app.include_router(test_router)
app.include_router(websocket_router)

@app.get("/")
def root():
    return {"message": "API Running Successfully"}