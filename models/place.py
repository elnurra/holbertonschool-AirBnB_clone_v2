#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from models.review import Review
from os import getenv
from sqlalchemy.orm import relationship
STO_TYP = getenv("HBNB_TYPE_STORAGE")

if STO_TYP == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    if STO_TYP == "db":
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []
        reviews = relationship('Review',
                               cascade="all, delete, delete-orphan",
                               backref="place")
        amenities = relationship("Amenity",
                                 secondary=place_amenity,
                                 back_populates='place_amenities',
                                 viewonly=False)

    else:
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []
        review_ids = []

        @property
        def reviews(self):
            from models import storage
            rev = []
            for x in storage.all(Review).values():
                if x.place_id == self.id:
                    rev.append(x)
            return rev

        @property
        def amenities(self):
            from models import storage
            from models.amenity import Amenity
            ame = []
            moby = storage.all(Amenity)

            for amenity_inst in moby.values():
                if amenity_inst.id == self.amenity_id:
                    ame.append(amenity_inst)
            return ame

        @amenities.setter
        def amenities(self, amenity_list):
            from models.amenity import Amenity
            for x in amenity_list:
                if type(x) == Amenity:
                    self.amenity_ids.append(x)

        @reviews.setter
        def reviews(self, review_obj):
            if review_obj and review_obj not in self.review_ids:
                self.review_ids.append(review_obj.id)
