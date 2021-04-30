import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, scoped_session

db_url = os.environ.get(
    'DATABASE_URL', 'postgres://jackson:password@localhost:5431/demo_stack')

engine = create_engine(db_url.replace(
    'postgres://', 'postgresql://', 1), echo=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
