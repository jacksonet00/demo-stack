from .engine import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, validates


class BaseModel:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())


class User(Base, BaseModel):
    __tablename__ = 'users'

    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    profile_photo = Column(String, unique=True, nullable=True)
    zoos = relationship('Zoo', back_populates='owner')
    animals = relationship('Animal', back_populates='owner')

    @validates('username')
    def convert_lowercase(self, key, value):
        return value.lower()


class Animal(Base, BaseModel):
    __tablename__ = 'animals'

    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    owner = relationship('User', back_populates='animals')
    zoo_id = Column(Integer, ForeignKey(
        'zoos.id', ondelete='SET NULL'), nullable=True)
    zoo = relationship('Zoo', back_populates='animals')


class Zoo(Base, BaseModel):
    __tablename__ = 'zoos'

    name = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    owner = relationship('User', back_populates='zoos')
    animals = relationship('Animal', back_populates='zoo')
