import json
""" Module  defines a class to manage file storage for the HBNB clone"""


class FileStorage:
    """ This class manages storage of the HBNB models in json format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary or list of objects of one type of class"""
        if cls is None:
            return FileStorage.__objects
        else:
            filtered_objects = {}
            for key, obj in FileStorage.__objects.items():
                if type(obj) == cls:
                    filtered_objects[key] = obj
            return filtered_objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = obj.__class__.__name__ + '.' + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        temp = {}
        for key, obj in FileStorage.__objects.items():
            temp[key] = obj.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)
    
    def delete(self, obj=None):
        """Deletes obj from __objects if it exists"""
        if obj is None:
            return
        key = obj.__class__.__name__ + '.' + obj.id
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]
         # if (obj is None):
        #     return

        # key = obj.__class__.__name__ + '.' + obj.id

        # try:
        #     del(self.all()[key])
        #     self.save()
        # except KeyError:
        #     print("** no instance found **")

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    class_name = val['__class__']
                    if class_name in classes:
                        obj = classes[class_name](**val)
                        FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass    
    
    def close(self):
        """ close method """
        self.reload()