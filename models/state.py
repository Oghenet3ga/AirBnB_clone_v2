#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import shlex
import models
from models.city import City


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        var = models.storage.all()
        list = []
        result = []
        for key in var:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if (city[0] == 'City'):
                list.append(var[key])
        for x in list:
            if (x.state_id == self.id):
                result.append(x)
        return (result)
