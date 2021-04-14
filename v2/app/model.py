import os
# from time import sleep
from sqlalchemy import create_engine, text, Integer, String, Column, MetaData, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine(os.environ['DATABASE_URL'].replace(
    'postgres://', 'postgresql://', 1))

Session = sessionmaker()
Session.configure(bind=engine)

db_session = Session()
Base = declarative_base()


class Animal(Base):
    __tablename__ = 'animal'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Animal(name='%s')>" % (self.name)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
