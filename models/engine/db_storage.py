#!/usr/bin/python3
""" defines the DBStorage class """

import os
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class DBStorage:
    """ manages MySQL database """
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.format(
            os.environ.get('HBNB_MYSQL_USER'),
            os.environ.get('HBNB_MYSQL_PWD'),
            os.environ.get('HBNB_MYSQL_HOST'),
            os.environ.get('HBNB_MYSQL_DB')
            ), pool_pre_ping=True)
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        if cls is not None:
            instances = self.__session.query(cls).all()
        else:
            instances = []
            for cls in [State, City, User, Place, Review]:
                instances.extend(self.__session.query(cls).all())
        all_instances = {}
        for instance in instances:
            all_instances['{}.{}'.format(instance.__class__.__name__, instance.id)] = instance
        return all_instances

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables and create the current database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
