from .engine import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    zoos = relationship('Zoo', back_populates='owner', )
    animals = relationship('Animal', back_populates='owner')


class Animal(Base):
    __tablename__ = 'animals'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship('User', back_populates='animals')
    zoo_id = Column(Integer, ForeignKey('zoos.id'), nullable=True)
    zoo = relationship('Zoo', back_populates='animals')


class Zoo(Base):
    __tablename__ = 'zoos'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    owner = relationship('User', back_populates='zoos')
    animals = relationship('Animal', back_populates='zoo')
