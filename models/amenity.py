#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ class amenity"""
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    from models.place import place_amenity
    place_amenities = relationship("Place",
                                   secondary=place_amenity)
