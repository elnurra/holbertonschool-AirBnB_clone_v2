#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

STO_TYP = getenv("HBNB_TYPE_STORAGE")
if STO_TYP == 'db':
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """A base class for all hbnb models"""
    if STO_TYP == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime,
                            default=datetime.utcnow(), nullable=False)
        updated_at = Column(DateTime,
                            default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {}
        kwargs.setdefault('id', str(uuid4()))
        kwargs.setdefault('created_at', datetime.utcnow())
        if not isinstance(kwargs['created_at'], datetime):
            kwargs['created_at'] = datetime.strptime(
                kwargs['created_at'], "%Y-%m-%d %H:%M:%S.%f"
            )
        kwargs.setdefault('updated_at', datetime.utcnow())
        if not isinstance(kwargs['updated_at'], datetime):
            kwargs['updated_at'] = datetime.strptime(
                kwargs['updated_at'], "%Y-%m-%d %H:%M:%S.%f"
            )
        if STO_TYP != 'db':
            kwargs.pop('__class__', None)
        for attr, val in kwargs.items():
            setattr(self, attr, val)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns dictionary of BaseModel"""
        cls_nam = self.__class__.__name__
        richard = {
            k: v if type(v) == str else str(v)
            for k, v in self.__dict__.items()
        }
        richard.update({
            '__class__': cls_nam
            })
        richard.pop("_sa_instance_state", None)
        return richard

    def delete(self):
        """deletes basemodel instance"""
        models.storage.delete(self)
