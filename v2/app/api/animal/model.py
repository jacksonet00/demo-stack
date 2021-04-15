from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ...engine import Base


class Animal(Base):
    __tablename__ = 'animals'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship('User', back_populates='animals')
    zoo_id = Column(Integer, ForeignKey('zoos.id'), nullable=True)
    zoo = relationship('Zoo', back_populates='animals')
