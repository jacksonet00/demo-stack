import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

db_url = os.environ.get(
    'DATABASE_URL') or 'postgres://jackson:password@localhost:5431/demo_stack'

engine = create_engine(db_url.replace(
    'postgres://', 'postgresql://', 1))

Session = sessionmaker()
Session.configure(bind=engine)

db_session = Session()
Base = declarative_base()
