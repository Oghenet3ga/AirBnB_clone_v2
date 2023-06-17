#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is not None:
            result = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    result[key] = value 
            return result
        else:
            return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        temp = {}
        for key, val in self.__objects.items():
            temp[key] = val.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    cls_name = val['__class__']
                    cls = self.classes.get(cls_name, None)
                    if cls is not None:
                        self.__objects[key] = cls(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside
        If obj is equal to None, the method should not do anything
        """
        if obj is None:
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        if key in self.__objects:
            del self.__objects[key]
            self.save()
