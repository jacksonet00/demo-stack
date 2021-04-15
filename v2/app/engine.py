import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine(os.environ['DATABASE_URL'].replace(
    'postgres://', 'postgresql://', 1))

Session = sessionmaker()
Session.configure(bind=engine)

db_session = Session()
Base = declarative_base()
