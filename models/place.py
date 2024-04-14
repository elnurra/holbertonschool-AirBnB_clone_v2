#!/usr/bin/python3
"""Defines the Place class."""
import os

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

import models
from models.amenity import Amenity
from models.base_model import Base, BaseModel
from models.review import Review

place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False,
    ),
)


class Place(BaseModel, Base):
    """Represents a Place for a MySQL database."""

    __tablename__ = "places"

    city_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("cities.id"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    number_rooms: Mapped[int] = mapped_column(default=0, nullable=False)
    number_bathrooms: Mapped[int] = mapped_column(default=0, nullable=False)
    max_guest: Mapped[int] = mapped_column(default=0, nullable=False)
    price_by_night: Mapped[int] = mapped_column(default=0, nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=True)
    longitude: Mapped[float] = mapped_column(nullable=True)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship(
        "Amenity", secondary=place_amenity, viewonly=False,
        overlaps="place_amenities"
    )

    amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE", None) != "db":

        @property
        def reviews(self):
            """Get a list of all linked Reviews."""
            review_list = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Get/set linked Amenities."""
            amenity_list = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)
