from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Index

from datetime import datetime

from app.db.base import Base


class Forecast(Base):

    __tablename__ = "forecasts"
    
    __table_args__ = (

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

    dataset_id = Column(
        Integer,
        ForeignKey("datasets.id"),
        index=True
    )
    
    
    
    predicted_value = Column(
        Float,
        nullable=False
    )

    prediction_date = Column(
        String(100),
        nullable=False
    )

    model_used = Column(
        String(100),
        index=True
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )