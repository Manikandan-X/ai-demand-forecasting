from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False,
        index=True
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    # ENTERPRISE ROLES
    # super_admin
    # analyst
    # viewer
    role = Column(
        String(50),
        default="viewer",
        index=True
    )

    # RELATIONSHIPS
    datasets = relationship(
        "Dataset",
        back_populates="user"
    )

    notifications = relationship(
        "Notification",
        back_populates="user"
    )

    forecasts = relationship(
        "ForecastHistory",
        back_populates="user"
    )