from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base
from app.db.session import engine

import app.models

from app.routers.auth import router as auth_router
from app.routers.dataset import router as dataset_router
from app.routers.forecast import router as forecast_router
from app.routers.dashboard import (
    router as dashboard_router
)
from app.routers.reports import (
    router as reports_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Demand Forecasting API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(dataset_router)
app.include_router(forecast_router)
app.include_router(dashboard_router)
app.include_router(reports_router)

@app.get("/")
def root():
    return {"message": "API Running Successfully"}