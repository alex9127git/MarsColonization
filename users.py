import datetime
from sqlalchemy import Column, String, Integer, DateTime, orm
from db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    position = Column(String, nullable=True)
    speciality = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    modified_date = Column(DateTime, default=datetime.datetime.now)
    job = orm.relationship("Jobs", back_populates="user")

    def __repr__(self):
        return f"{self.surname} {self.name} {self.age} {self.position} {self.speciality}\n" \
               f"{self.address} {self.email} {self.hashed_password}"
