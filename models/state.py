#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nulable=False)
    
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('city', backref='state', cascade='all, delete-orphan')
    else:
        @property
        def cities(self):
            """ """
            import models
            from models.city import City
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
