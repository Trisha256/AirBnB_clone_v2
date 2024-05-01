#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Review(BaseModel):
    """ Review classto store review information """
    __tablename__ = 'reviews'

    place_id = Column(String(60), ForeignKey
                      ('places_id'), nullable=False)
    user_id = Column(String(60), ForeignKey
                      ('users_id'), nullable=False)
    text = Column(String(1024), nullable=False)

