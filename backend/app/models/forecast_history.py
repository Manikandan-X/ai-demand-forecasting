from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Index

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db.base import Base


class ForecastHistory(Base):

    __tablename__ = "forecast_history"
    
    __table_args__ = (

        Index(
            "idx_forecast_user_created",
            "user_id",
            "created_at"
        ),

        Index(
            "idx_forecast_dataset_created",
            "dataset_id",
            "created_at"
        ),

    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        index=True
    )

    dataset_id = Column(
        Integer,
        ForeignKey("datasets.id"),
        index=True
    )

    model_name = Column(
        String(100),
        index=True
    )

    accuracy = Column(
        Float
    )
    
    confidence_score = Column(
        Float,
        default=0
    )

    forecast_result = Column(
        String(5000)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True

    )

    user = relationship(
        "User",
        back_populates="forecasts"
    )

    dataset = relationship(
        "Dataset",
        back_populates="forecasts"
    )