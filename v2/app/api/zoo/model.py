from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ...engine import Base


class Zoo(Base):
    __tablename__ = 'zoos'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    owner = relationship('User', back_populates='zoos')
    animals = relationship('Animal', back_populates='zoo')
