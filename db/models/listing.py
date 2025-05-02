from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from db.base import Base

if TYPE_CHECKING:
    from db.models import Realtor


class Listing(Base):
    """
    Database model for real estate listings posted by realtors.

    Attributes:
        id (int): Primary key.
        realtor_id (int): Foreign key referencing the realtor who created the listing.
        listing_type (str): Type of listing, either "rent" or "sale".
        rooms_count (int): Number of rooms in the property.
        address (str): Address of the listed property.
        floor (int): The floor on which the property is located.
        total_floors (int): Total number of floors in the building.
        area (float): Total area of the property in square meters.
        price (float): Listing price in the local currency.
        description (str | None): Optional textual description of the property.
        message_id (int | None): Telegram message ID of the post published in the channel.
        created_at (datetime): Timestamp of listing creation (UTC).

    Relationships:
        realtor (Realtor): Reference to the realtor who created the listing.
    """

    __tablename__ = "listing"

    id = Column(Integer, primary_key=True)
    realtor_id = Column(Integer, ForeignKey("realtor.id"), nullable=False)
    listing_type = Column(String, nullable=False)  # "rent" or "sale"
    rooms_count = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    floor = Column(Integer, nullable=True)
    total_floors = Column(Integer, nullable=True)
    area = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    message_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)

    realtor: Mapped["Realtor"] = relationship(
        "Realtor",
        back_populates="listings",
    )
