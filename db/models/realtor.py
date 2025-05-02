from datetime import UTC, date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, relationship

from db.base import Base

if TYPE_CHECKING:
    from db.models import Listing


class Realtor(Base):
    """
    Database model for realtors in the real estate agency.

    Attributes:
        id (int): Primary key.
        telegram_id (int): Unique Telegram user ID.
        first_name (str): First name of the realtor.
        last_name (str): Last name of the realtor.
        phone_number (str): Contact phone number.
        date_of_birth (date): Date of birth.
        created_at (datetime): Registration timestamp in UTC.
    """

    __tablename__ = "realtor"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC), nullable=False)

    listings: Mapped[list["Listing"]] = relationship(
        "Listing",
        back_populates="realtor",
    )
