import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

USER = os.getenv("HBNB_MYSQL_USER")
PASSWORD = os.getenv("HBNB_MYSQL_PWD")
HOST = os.getenv("HBNB_MYSQL_HOST")
DB = os.getenv("HBNB_MYSQL_DB")


class DBStorage:
    """
    This class represents the database storage for the AirBnB clone project.
    It provides methods to interact with the database, such as retrieving,
    creating, updating, and deleting objects.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes a new instance of the DBStorage class.
        It creates a database engine and drops all tables if the 'test'
        argument
        is present in the sys.argv list.
        """
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DB),
            pool_pre_ping=True,
        )
        if "test" in sys.argv:
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Retrieves all objects from the database.

        Args:
            cls (optional): The class of objects to retrieve. If not provided,
                            all objects from all classes will be retrieved.

        Returns:
            A dictionary of objects, where the key is in the format
            "<class_name>.<object_id>" and the value is the object itself.
        """
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) is str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(obj).__name__, obj.id): obj
                for obj in objs}

    def new(self, obj):
        """
        Adds a new object to the database session.

        Args:
            obj: The object to add to the session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits the changes made in the current session to the database.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the database session.

        Args:
            obj (optional): The object to delete. If not provided, no action
                            will be taken.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads the database session and creates all tables defined in the
        metadata.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Closes the current database session.
        """
        self.__session.close()
