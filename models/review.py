""" Review module for the HBNB project """

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base, BaseModel


class Review(BaseModel, Base):
    """Review class to store review information"""

    __tablename__ = "reviews"

    place_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("places.id"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("users.id"), nullable=False
    )
    text: Mapped[str] = mapped_column(String(1024), nullable=False)
