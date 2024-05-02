#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nulable=False)
    cities = relationship("City", cascade="delete", backref="state")
    
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('city', backref='state',
                              cascade='all, delete-orphan')
    else:
        @property
        def cities(self):
            """ cities getter attribute """
            import models
            from models.city import City
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
