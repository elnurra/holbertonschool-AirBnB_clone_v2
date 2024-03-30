#!/usr/bin/python3
""" """
import json
import models
import MySQLdb
import unittest
import os
from models import storage
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy import column, inspect, text
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine


@unittest.skipIf(type(models.storage) == FileStorage, "Testing FileStorage")
class TestDBStorage(unittest.TestCase):
    """ """

    @classmethod
    def setUpClass(cls):
        if type(models.storage) == DBStorage:
            cls.storage = DBStorage()
            Base.metadata.create_all(cls.storage._DBStorage__engine)
            Session = sessionmaker(bind=cls.storage._DBStorage__engine)
            cls.storage._DBStorage__session = Session()
            cls.state = State(name="Oklahoma")
            cls.storage._DBStorage__session.add(cls.state)
            cls.city = City(name="Tulsa", state_id=cls.state.id)
            cls.storage._DBStorage__session.add(cls.city)
            cls.user = User(email="5580@holbertonstudents.com", password="UWU")
            cls.storage._DBStorage__session.add(cls.user)
            cls.place = Place(city_id=cls.city.id, user_id=cls.user.id,
                              name="Hell")
            cls.storage._DBStorage__session.add(cls.place)
            cls.amenity = Amenity(name="Lacking")
            cls.storage._DBStorage__session.add(cls.amenity)
            cls.review = Review(place_id=cls.place.id, user_id=cls.user.id,
                                text="meh")
            cls.storage._DBStorage__session.add(cls.review)
            cls.storage._DBStorage__session.commit()

    @classmethod
    def tearDownClass(cls):
        if type(models.storage) == DBStorage:
            cls.storage._DBStorage__session.delete(cls.state)
            cls.storage._DBStorage__session.delete(cls.city)
            cls.storage._DBStorage__session.delete(cls.user)
            cls.storage._DBStorage__session.delete(cls.amenity)
            cls.storage._DBStorage__session.commit()
            del cls.state
            del cls.city
            del cls.user
            del cls.place
            del cls.amenity
            del cls.review
            cls.storage._DBStorage__session.close()
            del cls.storage

@unittest.skipIf(type(models.storage) == FileStorage, "Testing FileStorage")
class TestStateDBInstances(unittest.TestCase):
    """DBStorage State Tests"""

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        storage.hcf(State)

    def setUp(self):
        """initializes new BaseModel object for testing"""
        self.state = State()
        self.state.name = 'Oklahoma'
        self.state.save()

    def test_state_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = storage.all()
        all_state_objs = storage.all(State)
        exist_in_all = False
        for k in all_objs.keys():
            if self.state.id in k:
                exist_in_all = True
        exist_in_all_states = False
        for k in all_state_objs.keys():
            if self.state.id in k:
                exist_in_all_states = True
        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_states)

    def test_new_state(self):
        """... checks if new() functions after instantiation and save()"""
        actual = False
        self.s_new = State(name="NY")
        self.s_new.save()
        db_objs = storage.all()
        for obj in db_objs.values():
            if obj.id == self.s_new.id:
                actual = True
        self.assertTrue(actual)

    def test_state_delete(self):
        state_id = self.state.id
        storage.delete(self.state)
        storage.save()
        exist_in_all = False
        for k in storage.all().keys():
            if state_id in k:
                exist_in_all = True
        self.assertFalse(exist_in_all)


if __name__ == "__main__":
    unittest.main()
