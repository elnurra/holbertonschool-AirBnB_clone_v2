#!/usr/bin/python3
"""This module defines a class User"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_model import Base, BaseModel
from models.place import Place
from models.review import Review


class User(BaseModel, Base):
    """This class defines a user by various attributes"""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(128), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)
    places: Mapped["Place"] = relationship("Place", backref="user",
                                           cascade="delete")
    reviews: Mapped["Review"] = relationship("Review", backref="user",
                                             cascade="delete")
