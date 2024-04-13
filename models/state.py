#!/usr/bin/python3
""" State Module for HBNB project """
import models
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_model import Base, BaseModel
from models.city import City


class State(BaseModel, Base):
    """State Model"""

    __tablename__ = "states"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    cities: Mapped["City"] = relationship("City", backref="state",
                                          cascade="delete")

    @property
    def cities(self):
        """
            getter method, returns list of City objs from storage
            linked to the current State
        """
        city_list = []
        for city in models.storage.all("City").values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
