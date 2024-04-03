#!/usr/bin/python3
""" City Module for HBNB project """
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_model import Base, BaseModel
from models.place import Place


class City(BaseModel, Base):
    """The city class, contains state ID and name"""

    __tablename__ = "cities"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    state_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("states.id"), nullable=False
    )
    places: Mapped["Place"] = relationship("Place", backref="cities",
                                           cascade="delete")
