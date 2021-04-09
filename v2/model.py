from sqlalchemy import create_engine, text, Integer, String, Column, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('postgresql://jackson:password@localhost:5431/demo_stack')
Session = sessionmaker()
Session.configure(bind=engine)

db_session = Session()
Base = declarative_base()

engine.execute('''
CREATE TABLE IF NOT EXISTS animal (
  id SERIAL PRIMARY KEY,
  name TEXT
);
''')
class Animal(Base):
  __tablename__ = 'animal'

  id = Column(Integer, primary_key=True)
  name = Column(String)

  def __repr__(self):
    return "<Animal(name='%s')>" % (self.name)