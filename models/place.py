#!/usr/bin/python3
""" Place Module for HBNB project """ 
import models
from os import getenv
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False) 
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0) 
    number_bathrooms = Column(Integer, default=0) 
    max_guest = Column(Integer, default=0) 
    price_by_night = Column(Integer, default=0) 
    latitude = Column(Float, nullable=True) 
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", cascade='all, delete, delete-orphan',
                               backref="place")

        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        @property
        def reviews(self):
            """returns a list of reviews.id"""
            var = models.storage.all()
            list = []
            result = []
            for key in var:
                review = key.replace('.', ' ')
                review = shlex.split(review)
                if (review[0] == 'Review'):
                    list.append(var[key])
            for x in list:
                if (x.place_id == self.id):
                    result.append(x)
            return (result)

        @property
        def amenities(self):
            """returns a list of amenity id"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """adds amenity ids to the attr"""
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
