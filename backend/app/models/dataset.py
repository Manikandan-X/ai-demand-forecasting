from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

from app.db.base import Base


class Dataset(Base):

    __tablename__ = "datasets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String(255),
        nullable=False,
        index=True
    )

    file_path = Column(
        String(500),
        nullable=False
    )

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id"),
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    # RELATIONSHIP
    user = relationship(
        "User",
        back_populates="datasets"
    )

    forecasts = relationship(
        "ForecastHistory",
        back_populates="dataset"
    )