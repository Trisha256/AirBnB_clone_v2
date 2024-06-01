#!/usr/bin/python3
""" New engine DB storage"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.base_model import Base, BaseModel

classes = {
    'BaseModel': BaseModel, 'User': User, 'Place': Place,
    'State': State, 'City': City, 'Amenity': Amenity,
    'Review': Review
}


class DBStorage:
    """class database storage """
    __engine = None
    __session = None

    def __init__(self):
        """ The init method"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            os.getenv('HBNB_MYSQL_USER'),
            os.getenv('HBNB_MYSQL_PWD'),
            os.getenv('HBNB_MYSQL_HOST'),
            os.getenv('HBNB_MYSQL_DB')), pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ all method """
        objs_list = []
        if cls:
            if isinstance(cls, str):
                try:
                    cls = globals()[cls]
                except KeyError:
                    pass
            if issubclass(cls, Base):
                objs_list = self.__session.query(cls).all()
        else:
            for subclass in Base.__subclasses__():
                objs_list.extend(self.__session.query(subclass).all())
        
        obj_dict = {}
        for obj in objs_list:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            obj_dict[key] = obj
        return obj_dict
    
    def new(self, obj):
        """add object to the current
        database session(self.__session)
        """
        self.__session.add(obj)
    
    def save(self):
        """
        Commit the object to the current
        database session (self.__session)
        """
        self.__session.commit()
    
    def delete(self, obj=None):
        """ delete the object to the current
        database session (self.__session)
        """
        if obj:
            self.__session.delete(obj)
            self.save()
    
    def reload(self):
        """
        reload the object to the current database
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
    
    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()