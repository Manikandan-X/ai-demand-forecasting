from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db.base import Base


class ForecastHistory(Base):

    __tablename__ = "forecast_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    dataset_id = Column(
        Integer,
        ForeignKey("datasets.id")
    )

    model_name = Column(
        String(100)
    )

    accuracy = Column(
        Float
    )

    forecast_result = Column(
        String(5000)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="forecasts"
    )

    dataset = relationship(
        "Dataset",
        back_populates="forecasts"
    )