#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_model import Base, BaseModel


class Amenity(BaseModel, Base):
    """Amenity class that inherits from BaseModel"""

    __tablename__ = "amenities"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    place_amenities: Mapped["Place"] = relationship(
        "Place", secondary="place_amenity",
        overlaps="place_amenity", viewonly=False
    )
