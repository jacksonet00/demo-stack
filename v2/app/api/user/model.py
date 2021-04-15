from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ...engine import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    zoos = relationship('Zoo', back_populates='owner')
    animals = relationship('Animal', back_populates='owner')
