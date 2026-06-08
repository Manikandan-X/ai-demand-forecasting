from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Index

from sqlalchemy.orm import relationship

from app.db.base import Base
from sqlalchemy import Boolean

class User(Base):

    __tablename__ = "users"
    
    __table_args__ = (

        Index(
            "idx_user_email_role",
            "email",
            "role"
        ),

    )

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
    
    is_active = Column(
        Boolean,
        default=True,
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